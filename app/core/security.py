from passlib.context import CryptContext
from datetime import datetime,timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

# func: hash password
def hash_password(password:str ) -> str:
    """Hash password using bycrypt"""
    return pwd_context.hash(password)


# func: verify_password
def verify_password(plain_password:str, hashed_password:str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password,hashed_password)


# create access token
def create_access_token(data:dict, expires_delta: Optional[timedelta]= None) -> str:
    """Create JWT access token"""

    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)   
    return encoded_jwt   


# decode_access_token
def decode_access_token(token:str) -> Optional[dict]:
    """Decode JWT acess token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None