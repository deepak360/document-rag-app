from ollama import Client
import os
from app.core.config import settings

ollama = Client(host=settings.OLLAMA_BASE_URL)

def generate_answer(question: str, context_chunks: list[str]):
    prompt = f"""Use the context below to answer the question.
    Context:
    {"\n\n".join(context_chunks)}

    Question: {question}
    Answer:"""
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']
