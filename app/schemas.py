from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Tuple

from app.models import User


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    creator_id: int
    creator: UserResponse

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int | str] = None


class Vote(BaseModel):
    post_id: int
    vote_dir: int = 1 or 0
