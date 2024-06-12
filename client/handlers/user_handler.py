import jwt
from sqlalchemy.orm import Session
from client.models.models import User
from client.schemas.user_schema import UserUpdate, TokenData, User
from passlib.context import CryptContext
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
import datetime


SECRET_KEY = "b5d87730e943f1c259b00ea5a3760bcb82b3069bff0b3b91f4a14f8a16af7c2e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




"""Handlers"""

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, password):
    return password_context.verify(plain_password, password)


def get_password_hash(password):
    return password_context.hash(password)


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 3):
    return db.query(User).offset(skip).all()


def authenticate_user(db: Session, username : str, password : str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta : datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    access_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise access_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise access_exception 
    user = get_user(db, username=token_data.username)
    if user is None:
        raise access_exception
    return user


def create_user(db: Session, user: User): 
    password = get_password_hash(user.password)
    db_user = User(
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
    db_user = db.query(User).filter(User.id == user_id).first()
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
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
