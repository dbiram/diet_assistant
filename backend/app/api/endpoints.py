from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from app.rag.rag_engine import generate_answer
from fastapi import File, UploadFile
from app.vision.food_classifier import classify_food
from app.vision.nutrition_lookup import get_nutrition
from datetime import datetime

from sqlalchemy.orm import Session
from app.database import SessionLocal, MealLog, WorkoutLog
from app.api.schemas import MealLogInput, WorkoutLogInput

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    age: int
    gender: str 
    activity_level: str  # Example: "low", "moderate", "high"

@router.post("/ask_diet_assistant")
async def ask_diet_assistant(request: QuestionRequest):
    profile = {
        "age": request.age,
        "gender": request.gender,
        "activity_level": request.activity_level
    }
    answer = generate_answer(profile, request.question)
    return {"answer": answer}

@router.post("/estimate_nutrition_from_image")
async def estimate_nutrition_from_image(file: UploadFile = File(...)):
    label = classify_food(file.file)
    nutrition = get_nutrition(label)
    return {
        "label": label,
        "nutrition": nutrition
    }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/log_meal")
def log_meal(meal: MealLogInput, db: Session = Depends(get_db)):
    meal_entry = MealLog(**meal.dict())
    db.add(meal_entry)
    db.commit()
    db.refresh(meal_entry)
    return {"message": "Meal logged successfully", "id": meal_entry.id}

@router.post("/log_workout")
def log_workout(workout: WorkoutLogInput, db: Session = Depends(get_db)):
    workout_entry = WorkoutLog(**workout.dict())
    db.add(workout_entry)
    db.commit()
    db.refresh(workout_entry)
    return {"message": "Workout logged successfully", "id": workout_entry.id}

@router.get("/summary")
def get_summary(
    user_id: str,
    start_date: str = Query(None),
    end_date: str = Query(None),
    db: Session = Depends(get_db)
):
    # Parse date range if provided
    start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    # Filter meal logs
    meal_query = db.query(MealLog).filter(MealLog.user_id == user_id)
    if start:
        meal_query = meal_query.filter(MealLog.timestamp >= start)
    if end:
        meal_query = meal_query.filter(MealLog.timestamp <= end)
    meals = meal_query.all()

    # Filter workout logs
    workout_query = db.query(WorkoutLog).filter(WorkoutLog.user_id == user_id)
    if start:
        workout_query = workout_query.filter(WorkoutLog.timestamp >= start)
    if end:
        workout_query = workout_query.filter(WorkoutLog.timestamp <= end)
    workouts = workout_query.all()

    # Compute totals
    total_calories = sum(m.calories for m in meals)
    total_protein = sum(m.protein for m in meals)
    total_burned = sum(w.calories_burned for w in workouts)

    return {
        "user_id": user_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_calories_consumed": total_calories,
        "total_protein_consumed": total_protein,
        "total_calories_burned": total_burned
    }