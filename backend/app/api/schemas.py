from pydantic import BaseModel

class MealLogInput(BaseModel):
    food_name: str
    calories: float
    protein: float

class WorkoutLogInput(BaseModel):
    workout_type: str
    duration_minutes: float
    calories_burned: float
