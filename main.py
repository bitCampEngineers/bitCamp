from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from config.db import engine, SessionLocal
from client import models as client_models
from competition.models import competition as comp_models
from competition.models import task as task_models
from client import handler


client_models.Base.metadata.create_all(bind=engine)
comp_models.Base.metadata.create_all(bind=engine)
task_models.Base.metadata.create_all(bind=engine)

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



"""User Authentication"""


@app.get("/users/", response_model = List[handler.User])
def get_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = handler.get_users(db, skip=skip, limit=limit)
    return users



@app.post("/register/", response_model = handler.User)
def create_user(user: handler.UserCreate, db: Session = Depends(get_db)):
    db_user = handler.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, error_message = "Email already used")
    return handler.create_user(db=db, user=user)



@app.delete("/delete-users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, db: Session = Depends(get_db)):
    if not handler.delete_user(db=db, username=username):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

