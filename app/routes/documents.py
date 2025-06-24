from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os
from uuid import uuid4
from app.services.extractor import extract_text
from app.services.embedder import generate_embeddings
from app.models.document import Document
from app.schemas.document import UserFileOut
from app.db.sql import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_user_documents
from app.models.user import User
from app.models.file import File as FileMeta
from sqlalchemy.sql import select
from typing import List

router = APIRouter()

UPLOAD_DIR = "app/storage/documents"

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Save file locally
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(await file.read())

    # Extract text
    text = extract_text(filepath)
    if not text:
        raise HTTPException(status_code=400, detail="Failed to extract text")

    # Generate embeddings
    chunks, embeddings = generate_embeddings(text)

    # Save file metadata
    file = FileMeta(
        user_id=current_user.id,
        filename=file.filename,
        path=filepath,
    )
    db.add(file)
    await db.flush() 

    # Save metadata to DB
    for chunk, embedding in zip(chunks, embeddings):
        document = Document(
            file_id=file.id,
            chunks=[chunk],
            embedding=embedding,
        )
        db.add(document)
    await db.commit()

    return {"message": "Document uploaded"}

@router.get("/{user_id}", response_model=List[UserFileOut])
async def list_user_documents(user_id: int, db: AsyncSession = Depends(get_db)):
    documents = await get_user_documents(user_id, db)
    return documents
