from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy.orm import relationship
from .database import Base



class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  title = Column(String, index=True, nullable=False)
  slug = Column(String, unique=True, index=True, nullable=False)
  summary = Column(String)
  content = Column(JSONB, nullable=False)
  created_at = Column(
    DateTime(timezone=True), server_default=func.now()
  )

# class User(Base):
  