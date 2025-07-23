from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.rag_engine import generate_answer
from fastapi import File, UploadFile
from app.vision.food_classifier import classify_food
from app.vision.nutrition_lookup import get_nutrition

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