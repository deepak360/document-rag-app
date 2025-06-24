from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag import generate_answer

router = APIRouter()

class Query(BaseModel):
    question: str

@router.post("/")
async def answer_question(query: Query):
    try:
        response = await generate_answer(query.question)
        return {"question": query.question, "answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
