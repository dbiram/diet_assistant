from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from app.rag.rag_engine import generate_answer
from fastapi import File, UploadFile
from app.vision.food_classifier import classify_food
from app.vision.nutrition_lookup import get_nutrition
from datetime import datetime

from sqlalchemy.orm import Session
from app.database import MealLog, WorkoutLog, get_db
from app.api.schemas import MealLogInput, WorkoutLogInput
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.profile_models import UserProfile
from app.api.services import log_meal_entry, log_workout_entry, get_daily_summary, suggest_meal
from app.api.prompt_parser import parse_meal_prompt, parse_workout_prompt, detect_intent

router = APIRouter(prefix="/api")

class QuestionRequest(BaseModel):
    question: str
    age: int
    gender: str 
    activity_level: str  # Example: "low", "moderate", "high"

class ChatInput(BaseModel):
    prompt: str

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

@router.post("/log_meal")
def log_meal(meal: MealLogInput, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meal_entry = log_meal_entry(user=current_user, db=db, food_name=meal.food_name, calories=meal.calories, protein=meal.protein)
    db.add(meal_entry)
    db.commit()
    db.refresh(meal_entry)
    return {"message": "Meal logged successfully", "id": meal_entry.id}

@router.post("/log_workout")
def log_workout(workout: WorkoutLogInput, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workout_entry = log_workout_entry(user=current_user, db=db, workout_type=workout.workout_type, duration_minutes=workout.duration_minutes, calories_burned=workout.calories_burned)
    db.add(workout_entry)
    db.commit()
    db.refresh(workout_entry)
    return {"message": "Workout logged successfully", "id": workout_entry.id}

@router.get("/summary/today")
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = datetime.utcnow().date()
    return get_daily_summary(current_user, db, today)

@router.post("/chat")
def chat(
    input: ChatInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prompt = input.prompt.strip()
    intent = detect_intent(prompt)
    
    if intent == "meal_log":
        parsed_items = parse_meal_prompt(prompt)
        if not parsed_items:
            return {"response": "Sorry, I couldn't recognize any food items."}
        
        for item in parsed_items:
            log_meal_entry(
                user=current_user,
                db=db,
                food_name=item["food_name"],
                calories=item["calories"],
                protein=item["protein"]
            )
        return {"response": f"Logged {len(parsed_items)} meal item(s)."}

    elif intent == "workout_log":
        parsed_workouts = parse_workout_prompt(prompt)
        if not parsed_workouts:
            return {"response": "Sorry, I couldn't recognize the workout details."}
        
        for workout in parsed_workouts:
            log_workout_entry(
                user=current_user,
                db=db,
                workout_type=workout["workout_type"],
                duration_minutes=workout["duration_minutes"],
                calories_burned=workout["calories_burned"]
            )
        return {"response": f"Logged {len(parsed_workouts)} workout(s)."}

    elif intent == "summary":
        today = datetime.utcnow().date()
        summary = get_daily_summary(current_user, db, today)
        return {"response": summary}

    elif intent == "suggestion":
        suggestion = suggest_meal(current_user, db)
        return {"response": suggestion}

    else:  # rag_question fallback
        profile = db.query(UserProfile).filter_by(user_id=current_user.id).first()
        if not profile:
            return {"response": "Please set up your profile first."}
        profile_dict = {
            "age": profile.age,
            "gender": profile.gender,
            "activity_level": profile.activity_level
        }
        answer = generate_answer(profile_dict, prompt)
        return {"response": answer}