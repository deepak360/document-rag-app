from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings

# Create SQLAlchemy engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG_MODE,
    future=settings.FUTURE
)

# Create session factory
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Create base class for models
Base = declarative_base()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency for FastAPI routes
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
