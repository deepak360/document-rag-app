# app/api/routes/qa.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from app.services.retriever import get_relevant_chunks
from app.services.llm import generate_answer

router = APIRouter()

class QARequest(BaseModel):
    question: str
    user_id: int

class QAResponse(BaseModel):
    answer: str
    sources: List[str]  # Or List[dict] with {chunk, filename}

@router.post("/ask", response_model=QAResponse)
async def ask_question(data: QARequest):
    # 1. Retrieve relevant chunks
    chunks = await get_relevant_chunks(data.question, user_id=data.user_id)

    # 2. Call LLM to generate answer
    answer = generate_answer(question=data.question, context_chunks=chunks)

    return QAResponse(
        answer=answer,
        sources=chunks  # You can return source text or add filenames
    )