from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(
    autocommit= False,
    autoflush= False,
    bind=engine,
    expire_on_commit=False

)

Base = declarative_base()

from fastapi.exceptions import HTTPException

def get_db():
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    except HTTPException:
        # ไม่ catch HTTPException
        raise
    except Exception as e:
        logger.error(f"Database error: {str(e)}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()