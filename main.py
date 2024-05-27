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


@app.get("/users/{user_id}",response_model= handler.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = handler.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/register/", response_model = handler.User)
def create_user(user: handler.UserCreate, db: Session = Depends(get_db)):
    db_user = handler.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, error_message = "Username already used")
    return handler.create_user(db=db, user=user)


@app.put("/users/{user_id}/", response_model= handler.User)
def update_user(user_id: int, user_update: handler.UserUpdate, db: Session = Depends(get_db)):
    updated_user = handler.update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.delete("/delete-users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, db: Session = Depends(get_db)):
    if not handler.delete_user(db=db, username=username):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


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


