from sqlalchemy import create_engine, Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
import json

from app.config import get_settings

settings = get_settings()

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    title = Column(String)
    description = Column(String, nullable=True)  # Original post caption/description
    source_url = Column(String)
    source_type = Column(String)
    data = Column(JSON)  # Stores the full recipe JSON from AI
    thumbnail_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    imported_at = Column(DateTime, default=datetime.utcnow)

class ImportJob(Base):
    __tablename__ = "import_jobs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    source_url = Column(String)
    status = Column(String, default="processing")  # processing, completed, failed
    error_message = Column(String, nullable=True)
    recipe_id = Column(String, ForeignKey("recipes.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
