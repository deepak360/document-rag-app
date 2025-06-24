from sqlalchemy import Column, Text, JSON, DateTime, ForeignKey, Integer
from app.db.sql import Base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    chunks = Column(JSON, nullable=False)
    embedding = Column(Vector(384))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    file = relationship("File", back_populates="documents")