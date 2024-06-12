from typing import Optional
from pydantic import BaseModel



class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    username : str | None = None


class UserBase(BaseModel):
    username: str
    points: int
    is_active: bool = True
    solved_tasks: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    points: Optional[int] = None
    solved_tasks: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True