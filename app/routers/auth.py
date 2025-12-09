from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from datetime import timedelta
from app import models,schemas
from app.database import get_db
from app.core.security import hash_password,verify_password,create_access_token
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register",response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user:schemas.UserCreate, db:Session=Depends(get_db)):
    """Register a new user"""

    # Check if user exists
    existing_user = db.query(models.User).filter((models.User.email == user.email) | (models.User.username == user.username)).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email or username already registered")
    
    # Create new user
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name = user.full_name,
        hashed_password = hash_password(user.password)
        )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info(f"New user registered: {db_user.email}")
    return db_user


@router.post("/login", response_model=schemas.Token)
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Login user and return JWT token"""
    db_user = db.query(models.User).filter(models.User.email == email).first()
    
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {db_user.email}")
    
    return {"access_token": access_token, "token_type": "bearer", "user": db_user}
    