from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(...,min_length=1, max_length=255)
    content: str = Field(...,min_length=1, max_length=5000)


class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1, max_length=5000)


class PostOut(PostBase):
    id: int
    owner_id : int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes : True


class PostDetailOut(PostBase):
    id: int
    owner_id :int
    created_at: datetime
    updated_at: datetime
    owner: "UserOut"

    class Config:
        from_attributes: True

from app.schemas.user import UserOut
PostDetailOut.model_rebuild()