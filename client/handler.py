from sqlalchemy.orm import Session
from pydantic import BaseModel
from .models import models


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True




def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 3):
    return db.query(models.User).offset(skip).all()


def create_user(db: Session, user: UserCreate): 
    """
    It is not completed. Researching how to hash and coming back to compelte you.
    """
    password = user.password
    db_user = models.User(username=user.username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



