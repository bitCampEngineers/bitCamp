from client.models import models
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from client import handler
from config.db import engine, SessionLocal
from typing import Optional
from random import randint

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users/", response_model = handler.User)
def create_user(user: handler.UserCreate, db: Session = Depends(get_db)):
    db_user = handler.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, error_message = "Email already used")
    return handler.create_user(db=db, user=user)

@app.get("/users/", response_model = handler.User)
def get_user(db: Session = Depends(get_db)):
    users = handler.get_users(db)
    if users:
        return {
            "success": "True",
            "status_code": "200",
            "users": users
            }
    return {
        "success": "False",
        "status_code": "404",
    }

@app.get("/get-task/",  status_code=status.HTTP_200_OK)
def get_user(count: int = 1, types: str = 'Easy'):
    response = []
    def get_task():
        return randint(0, 1827)
    
    
    while count > 0:
        response.append(get_task())
        count -= 1
    
    return {
        "success": "True",
        "result": response
    }


