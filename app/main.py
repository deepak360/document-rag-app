from fastapi import FastAPI
from app.core.config import settings
from app.db.sql import create_tables, SessionLocal, engine
from sklearn.feature_extraction.text import TfidfVectorizer
from app.models.document import Document
from sqlalchemy import select as SELECT, text
from sqlalchemy.exc import OperationalError
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as api_router
import asyncio
import pickle

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await wait_for_db(engine)
    await create_tables()
    # await train_and_save_vocab()
    yield
    # Optional: add shutdown logic here



app = FastAPI(
    title="Document Management and RAG-based Q&A",
    description="Ingest documents, generate embeddings, and query using RAG.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/")
def health_check():
    return {"status": "Running", "message": "Welcome to the RAG-based Q&A API"}

async def train_and_save_vocab():
    async with SessionLocal() as session:
        result = await session.execute(SELECT(Document.chunks))
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
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                print("Database is ready.")
                return
        except OperationalError as e:
            print(f"Database not ready yet. Retrying ({i+1}/{retries})...")
            await asyncio.sleep(delay)
    raise Exception("Database connection failed after multiple retries")
