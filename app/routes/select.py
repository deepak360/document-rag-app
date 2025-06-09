from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class SelectionRequest(BaseModel):
    doc_ids: List[str]

@router.post("/")
async def select_documents(payload: SelectionRequest):
    # Simulate document selection
    return {"selected_documents": payload.doc_ids, "status": "Selection updated"}
