from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import models
from passlib.context import CryptContext
from typing import Optional



"""Pydantic models"""

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


"""Handlers"""

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, password):
    return password_context.verify(plain_password, password)


def get_password_hash(password):
    return password_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 3):
    return db.query(models.User).offset(skip).all()


def create_user(db: Session, user: User): 
    """
    It is not completed. Researching how to hash and coming back to compelte you.
    """
    password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, 
        password=password, points=user.points, 
        is_active=user.is_active, 
        solved_tasks=user.solved_tasks
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    # Fetch the user from the database
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        return None
    
    # Update the fields if they are provided

    if user_update.username is not None:
        db_user.username = user_update.username
    
    if user_update.password is not None:
        db_user.password = get_password_hash(user_update.password)

    if user_update.points is not None:
        db_user.points = user_update.points
    
    if user_update.solved_tasks is not None:
        db_user.solved_tasks = user_update.solved_tasks


    db.commit()
    db.refresh(db_user)
    
    return db_user

def delete_user(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False



