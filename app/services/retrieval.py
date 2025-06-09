# retrieval.py
from sqlalchemy.future import select
from app.database import SessionLocal
from app.models import document
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import asyncio
from app.services.embedding import generate_embedding

async def retrieve_documents(question: str, top_k: int = 3):
    # Step 1: Generate embedding for the input question
    question_vector = await generate_embedding(question)

    # Step 2: Fetch all documents with embeddings from DB
    async with SessionLocal() as session:
        result = await session.execute(select(document.Document))
        docs = result.scalars().all()

        scored_docs = []
        for doc in docs:
            if doc.embedding:
                score = cosine_similarity(
                    [question_vector],
                    [doc.embedding]
                )[0][0]
                scored_docs.append((score, doc.content))

        # Step 3: Sort by score and return top K documents
        top_docs = sorted(scored_docs, key=lambda x: x[0], reverse=True)[:top_k]
        return [content for _, content in top_docs]
