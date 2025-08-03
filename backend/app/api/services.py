from sqlalchemy.orm import Session
from app.database import MealLog, WorkoutLog
from app.auth.models import User
from datetime import datetime, date
from app.auth.profile_models import UserProfile
from app.vision.nutrition_lookup import NUTRITION_TABLE

def log_meal_entry(user: User, db: Session, food_name: str, calories: float, protein: float, timestamp: datetime = None) -> MealLog:
    meal_entry = MealLog(
        user_id=user.id,
        food_name=food_name,
        calories=calories,
        protein=protein,
        timestamp=timestamp or datetime.utcnow()
    )
    db.add(meal_entry)
    db.commit()
    db.refresh(meal_entry)
    return meal_entry


def log_workout_entry(user: User, db: Session, workout_type: str, duration_minutes: float, calories_burned: float, timestamp: datetime = None) -> WorkoutLog:
    workout_entry = WorkoutLog(
        user_id=user.id,
        workout_type=workout_type,
        duration_minutes=duration_minutes,
        calories_burned=calories_burned,
        timestamp=timestamp or datetime.utcnow()
    )
    db.add(workout_entry)
    db.commit()
    db.refresh(workout_entry)
    return workout_entry

def get_daily_summary(user: User, db: Session, day: date = None):
    """
    Return calories consumed, protein, and calories burned for a given user on a given date.
    """
    if day is None:
        day = datetime.utcnow().date()
    start = datetime.combine(day, datetime.min.time())
    end = datetime.combine(day, datetime.max.time())

    meals = (
        db.query(MealLog)
        .filter(MealLog.user_id == user.id)
        .filter(MealLog.timestamp >= start)
        .filter(MealLog.timestamp <= end)
        .all()
    )

    workouts = (
        db.query(WorkoutLog)
        .filter(WorkoutLog.user_id == user.id)
        .filter(WorkoutLog.timestamp >= start)
        .filter(WorkoutLog.timestamp <= end)
        .all()
    )

    total_calories = sum(m.calories for m in meals)
    total_protein = sum(m.protein for m in meals)
    total_burned = sum(w.calories_burned for w in workouts)

    return {
        "date": day.isoformat(),
        "total_calories_consumed": total_calories,
        "total_protein_consumed": total_protein,
        "total_calories_burned": total_burned,
        "meals": [m.food_name for m in meals],
        "workouts": [w.workout_type for w in workouts]
    }

def get_nutrition_gap(user: User, db: Session, day: date = None):
    profile = db.query(UserProfile).filter_by(user_id=user.id).first()
    if not profile:
        return None

    if day is None:
        day = datetime.utcnow().date()
    summary = get_daily_summary(user, db, day)

    # Check if it's a workout day (based on WorkoutLog presence)
    is_workout_day = len(summary["workouts"]) > 0

    cal_target = profile.calories_workout_day if is_workout_day else profile.calories_rest_day
    prot_target = profile.protein_grams_workout_day if is_workout_day else profile.protein_grams_rest_day

    cal_gap = cal_target - summary["total_calories_consumed"]
    prot_gap = prot_target - summary["total_protein_consumed"]

    return {
        "is_workout_day": is_workout_day,
        "target_calories": cal_target,
        "target_protein": prot_target,
        "calories_gap": max(0, cal_gap),
        "protein_gap": max(0, prot_gap)
    }

def suggest_meal(user: User, db: Session) -> str:
    gap = get_nutrition_gap(user, db)
    if not gap:
        return "You need to set up your profile first."

    if gap["calories_gap"] < 100 and gap["protein_gap"] < 5:
        return "You've already met your targets for today! ✅"

    suggestions = []
    for food, info in NUTRITION_TABLE.items():
        cal = float(info.get("calories", 0) or 0)
        prot = float(info.get("protein", 0) or 0)
        if cal > 0 and prot > 0:
            score = (prot / gap["protein_gap"]) + (cal / gap["calories_gap"])
            suggestions.append((food, cal, prot, score))

    suggestions.sort(key=lambda x: x[3])  # smallest gap = best fit
    top_foods = suggestions[:3]

    lines = [f"You still need ~{gap['calories_gap']:.0f} kcal and {gap['protein_gap']:.0f}g protein."]
    lines.append("Here are some suggested foods to help you hit your goal:")
    for food, cal, prot, _ in top_foods:
        lines.append(f"• {food.title()}: {int(cal)} kcal, {int(prot)}g protein")

    return "\n".join(lines)
