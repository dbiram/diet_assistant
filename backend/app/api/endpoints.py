from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.rag_engine import generate_answer

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask_diet_assistant")
async def ask_diet_assistant(request: QuestionRequest):
    answer = generate_answer(request.question)
    return {"answer": answer}