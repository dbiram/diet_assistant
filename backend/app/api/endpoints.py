from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.rag_engine import generate_answer

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