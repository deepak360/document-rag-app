from sqlalchemy import Column, ForeignKey, Integer, String
from app.db.sql import Base
from sqlalchemy.orm import relationship

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    feature = Column(String, unique=True)
    description = Column(String)

class RolePermission(Base):
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True)
    role = Column(String)
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    permission = relationship("Permission")