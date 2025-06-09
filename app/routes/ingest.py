from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.embedding import generate_embedding
from app.models import document
from app.database import SessionLocal

router = APIRouter()

class Document(BaseModel):
    doc_id: str
    content: str
    title: str

@router.post("/")
async def ingest_document(doc: Document):
    try:
        embedding = await generate_embedding(doc.content)
        # Store the embedding with doc_id in DB (mock for now)
        async with SessionLocal() as session:
            new_doc = document.Document(
                id=doc.doc_id,
                title=doc.title,
                content=doc.content,
                embedding=embedding
            )
            session.add(new_doc)
            await session.commit()

        return {"doc_id": doc.doc_id, "embedding": embedding[:5], "message": "Ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
