from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import hash_password
from app.dependencies import get_current_user
from app.database import get_db
import logging
from typing import List


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["posts"])



@router.post("/",response_model=schemas.PostOut,status_code=status.HTTP_201_CREATED)
def create_post(post : schemas.PostCreate,db: Session = Depends(get_db) ,current_user: models.User = Depends(get_current_user)):
    """Create a new post"""

    db_post = models.Post(title = post.title,content = post.content, owner_id = current_user.id )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    logger.info(f"Post created: {db_post.id} by user {current_user.id}")
    return db_post



@router.get("/",response_model=List[schemas.PostDetailOut])
def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)):

    """Get all post with pagination"""
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

    return posts

@router.get("/{post_id}",response_model=schemas.PostDetailOut)
def get_post(post_id:int, db: Session = Depends(get_db)):
    """Get single post bt ID"""

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
    
    return post


@router.put("/{post_id}",response_model=schemas.PostOut)
def update_post(post_id:int, post_update : schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Update a post (owner only)"""

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    
    # Check Ownership
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to update this post")
    
    # Update fields
    if post_update.title:
        post.title  = post_update.title
    if post_update.content:
        post.content = post_update.content

    db.commit()
    db.refresh(post)

    logger.info(f"Post updated: {post.id}")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int, db : Session = Depends(get_db) , current_user : models.User = Depends(get_current_user)):
    """Delete a post (owner only)"""

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    
    # Check Ownership
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="No authorized to delete this post")
    
    db.delete(post)
    db.commit()

    logger.info(f"Post Deleted: {post_id}")
    return None


@router.get("/user/{user_id}", response_model=List[schemas.PostOut])
def get_user_posts(
    user_id : int,
    db : Session = Depends(get_db),
    skip : int = Query(0, ge=0),
    limit : int = Query(10, ge=1, le=100)
    ):
    """Get all post by user_id """

    # Check if user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    posts = db.query(models.Post).filter(models.Post.owner_id == user_id).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()

    return posts

