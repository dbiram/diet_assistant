from sqlalchemy.orm import Session
from app.database import MealLog, WorkoutLog
from app.auth.models import User
from datetime import datetime

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