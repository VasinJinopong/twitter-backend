from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user
from app.core.security import hash_password
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users",tags=["users"])

@router.get("/me",response_model=schemas.UserOut)
def get_current_user_info(current_user: models.User  = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.get("/{user_id}",response_model=schemas.UserOut)
def get_user(user_id:int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    return user


@router.put("/me",response_model=schemas.UserOut)
def update_current_user(user_update : schemas.UserUpdate, db:Session = Depends(get_db),current_user : models.User = Depends(get_current_user) ):
    """Update current user information"""

    # Check if email is already taken
    if user_update.email and user_update.email != current_user.email:
        existing = db.query(models.User).filter(models.User.email == user_update.email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already in use")
        
    # Update fields
    if user_update.email:
        current_user.email = user_update.email

    if user_update.full_name:
        current_user.full_name = user_update.full_name

    if user_update.password:
        current_user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(current_user)

    logger.info(f"User updated: {current_user.email}")
    return current_user


@router.delete("/me",status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(db: Session = Depends(get_db),current_user : models.User = Depends(get_current_user)):
    """Delete current user account"""

    db.delete(current_user)
    db.commit()

    logger.info(f"User deleted: {current_user.email}")
    return None
