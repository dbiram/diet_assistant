from pydantic import BaseModel

class MealLogInput(BaseModel):
    user_id: str
    food_name: str
    calories: float
    protein: float

class WorkoutLogInput(BaseModel):
    user_id: str
    workout_type: str
    duration_minutes: float
    calories_burned: float
