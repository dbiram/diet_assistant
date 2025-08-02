from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    age = Column(Integer)
    gender = Column(String)
    weight_kg = Column(Float)
    height_cm = Column(Float)
    activity_level = Column(String)  # "low", "moderate", "high"
    target_weight_kg = Column(Float)
    timeframe_weeks = Column(Integer)
    workouts_per_week = Column(Integer)

    # Target intake (computed)
    calories_workout_day = Column(Integer)
    calories_rest_day = Column(Integer)
    protein_grams_workout_day = Column(Integer)
    protein_grams_rest_day = Column(Integer)
