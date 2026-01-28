from sqlalchemy import create_engine, Column, String, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import JSON
from datetime import datetime
import uuid

from app.config import get_settings

settings = get_settings()

# Create database engine (supports both SQLite and PostgreSQL)
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False}  # SQLite specific
    )
    # Use JSON for SQLite
    JSONType = JSON
else:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    # Use JSONB for PostgreSQL
    JSONType = JSONB



# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class Recipe(Base):
    """Recipe model with JSON storage for structured data"""
    __tablename__ = "recipes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    
    # Basic info
    title = Column(String(255), nullable=False)
    source_url = Column(Text, nullable=False)
    source_type = Column(String(50), default="instagram_reel")
    
    # Structured recipe data (ingredients, steps, etc.)
    data = Column(JSONType, nullable=False)
    
    # Media URLs
    thumbnail_url = Column(Text)
    video_url = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    imported_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_recipes_user', 'user_id'),
    )


class ImportJob(Base):
    """Track recipe import jobs for monitoring and retries"""
    __tablename__ = "import_jobs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    
    # Job details
    source_url = Column(Text, nullable=False)
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    
    # Result
    recipe_id = Column(String(36), nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Retry tracking
    attempts = Column(String(50), default="0")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


def get_db():
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
