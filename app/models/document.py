from sqlalchemy import Column, String, Text, JSON, DateTime
from app.database import Base
from sqlalchemy.sql import func

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())