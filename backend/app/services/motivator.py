from sqlalchemy.orm import Session
from app.api.services import get_nutrition_gap
from app.auth.models import User
from datetime import date, timedelta, datetime

def get_motivation(user: User, db: Session, day: date = None) -> str:
    """
    Returns a short motivational message based on today's summary and profile.
    """
    gap_info = get_nutrition_gap(user, db, day)
    if not gap_info:
        return "Let’s set up your profile to get personalized tips!"

    calorie_gap = gap_info["calories_gap"]
    protein_gap = gap_info["protein_gap"]

    if calorie_gap > 300:
        return "You're behind on calories today. Time to refuel!"
    elif calorie_gap == 0:
        return "You’ve gone a bit over your calorie goal. A light dinner might balance it out. "

    if protein_gap > 20:
        return f"You still need about {protein_gap:.0f}g of protein — maybe a Greek yogurt or eggs?"

    return "You're crushing your nutrition goals today — keep it up!"

def get_streak(user: User, db: Session, max_days: int = 30) -> int:
    """
    Count consecutive days the user hit both calorie and protein targets.
    Looks backward from today, up to max_days.
    """
    today = datetime.utcnow().date()
    streak = 0

    for i in range(max_days):
        check_day = today - timedelta(days=i)
        gap_info = get_nutrition_gap(user, db, day=check_day)

        if not gap_info:
            break  # No profile or no data

        if gap_info["calories_gap"] <= 200 and gap_info["protein_gap"] <= 10:
            streak += 1
        else:
            break  # Streak broken

    return streak

def build_response(summary, suggestion, motivation, streak_msg):
    meals = summary.get("total_calories_consumed", 0)
    protein = summary.get("total_protein_consumed", 0)
    burned = summary.get("total_calories_burned", 0)

    msg = f"📊 You've consumed **{meals} kcal** and **{protein}g protein** today.\n"
    if burned > 0:
        msg += f"🔥 You've burned **{burned} kcal** from workouts.\n"

    if suggestion:
        msg += suggestion + "\n"

    if motivation:
        msg += f"💪 {motivation}\n"

    if streak_msg:
        msg += f"\n🌟 {streak_msg}"

    return msg