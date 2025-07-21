# app/rag/retriever.py
from sentence_transformers import SentenceTransformer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np
from app.models.document import Document
from app.db.sql import get_db
from typing import List
from app.models.file import File

model = SentenceTransformer("BAAI/bge-small-en-v1.5")  # Match your embedding model

async def get_relevant_chunks(question: str, user_id: int, top_k: int = 3) -> List[str]:
	q_embedding = model.encode(question).tolist()
	
	db = await anext(get_db())#retrieve the first item from an async generator
	result = await db.execute(
		select(Document).join(File).filter(File.user_id == user_id)
	)
	docs = result.scalars().all()

	scores = []
	for doc in docs:
		if doc.embedding is None:
			continue
		try:
			#Computes cosine similarity between the query and document embeddings.
			score = np.dot(q_embedding, doc.embedding) / (
				np.linalg.norm(q_embedding) * np.linalg.norm(doc.embedding)
			)
			# score is a float between -1 and 1.
			scores.append((score, doc))
		except Exception as e:
			print(f"Error computing score for doc {doc.id}: {e}")

	top_matches = sorted(scores, key=lambda x: x[0], reverse=True)[:top_k]
	return [doc.chunks[0] for _, doc in top_matches if doc.chunks]