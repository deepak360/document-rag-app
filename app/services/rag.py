import asyncio
from app.services.retrieval import retrieve_documents

async def generate_answer(question: str) -> str:
    docs = await retrieve_documents(question)
    context = " ".join(docs)
    return f"Answer based on retrieved docs: {context[:100]}..."
