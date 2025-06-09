from fastapi import FastAPI
from app.routes import ingest, qa, select
from app.database import create_tables, SessionLocal, engine

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from app.models.document import Document
from sqlalchemy import select as SELECT
import asyncio
from sqlalchemy.exc import OperationalError
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await wait_for_db(engine)
    await create_tables()
    await train_and_save_vocab()
    yield
    # Optional: add shutdown logic here



app = FastAPI(
    title="Document Management and RAG-based Q&A",
    description="Ingest documents, generate embeddings, and query using RAG.",
    version="1.0.0",
    lifespan=lifespan
)

# Include route modules
#This url save data and their embeddings to DB
app.include_router(ingest.router, prefix="/ingest", tags=["Document Ingestion"])
#This url is for Ques-Ans we pass Ques and get Ans.
app.include_router(qa.router, prefix="/qa", tags=["Q&A"])
app.include_router(select.router, prefix="/select-documents", tags=["Document Selection"])

@app.get("/")
def health_check():
    return {"status": "Running", "message": "Welcome to the RAG-based Q&A API"}

async def train_and_save_vocab():
    async with SessionLocal() as session:
        result = await session.execute(SELECT(Document.content))
        contents = result.scalars().all()
    
    if contents:
        vectorizer = TfidfVectorizer()
        vectorizer.fit(contents)

        with open("vocabulary/tfidf_vocab.pkl", "wb") as f:
            pickle.dump(vectorizer.vocabulary_, f)

async def wait_for_db(engine, retries=5, delay=2):
    for i in range(retries):
        try:
            async with engine.begin() as conn:
                return
        except OperationalError as e:
            print(f"Database not ready yet. Retrying ({i+1}/{retries})...")
            await asyncio.sleep(delay)
    raise Exception("Database connection failed after multiple retries")
