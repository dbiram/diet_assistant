from pydantic import BaseModel

class ProfileCreate(BaseModel):
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    activity_level: str  # "low", "moderate", "high"
    target_weight_kg: float
    timeframe_weeks: int
    workouts_per_week: int

class ProfileResponse(ProfileCreate):
    calories_workout_day: int
    calories_rest_day: int
    protein_grams_workout_day: int
    protein_grams_rest_day: int
