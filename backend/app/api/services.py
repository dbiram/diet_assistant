from sqlalchemy.orm import Session
from app.database import MealLog, WorkoutLog
from app.auth.models import User
from datetime import datetime, date

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