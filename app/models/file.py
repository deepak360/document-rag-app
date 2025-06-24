from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from app.db.sql import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    documents = relationship("Document", back_populates="file", cascade="all, delete-orphan")
    user = relationship("User", back_populates="files")