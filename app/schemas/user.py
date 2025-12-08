from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import Optional

class UserBase(BaseModel):
    email : EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    email : EmailStr
    password : str


class UserUpdate(BaseModel):
    email: Optional[EmailStr]= None
    full_name: Optional[str] = Field(None,max_length=255)
    password: Optional[str] = Field(None, min_length=8)


class UserOut(UserBase):
    id : int
    is_active: bool
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token:str
    token_type : str = "bearer"
    user: UserOut
