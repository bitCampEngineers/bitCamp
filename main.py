from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from client import models, handler
from config.db import engine, SessionLocal




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
