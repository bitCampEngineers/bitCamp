from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import datetime
from config.db import engine, SessionLocal
from client import models as client_models
from competition.models import competition as comp_models
from competition.models import task as task_models
from competition.models import case as case_models
from competition.models import input as input_models
from client import handler


client_models.Base.metadata.create_all(bind=engine)
comp_models.Base.metadata.create_all(bind=engine)
task_models.Base.metadata.create_all(bind=engine)
case_models.Base.metadata.create_all(bind=engine)
input_models.Base.metadata.create_all(bind=engine)


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
<<<<<<< HEAD
    return {"message": "Hello World"}



"""User Authentication"""


@app.get("/users/", response_model = List[handler.User])
def get_users(token: Annotated[str, Depends(handler.oauth2_scheme)],skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = handler.get_users(db, skip=skip, limit=limit)
    return users, token


@app.get("/users/{user_id}",response_model= handler.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = handler.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("users/register/", response_model = handler.User)
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


@app.delete("/users/delete/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, db: Session = Depends(get_db)):
    if not handler.delete_user(db=db, username=username):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


@app.post("/users/token")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(),
) -> handler.Token:
    user = handler.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=handler.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = handler.create_access_token(
        data = {"sub": user.username}, expires_delta=access_token_expires
    )
    return handler.Token(access_token=access_token, token_type="bearer")


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


=======
    return {"message": "IYA FEZURBEK otlamen"}
>>>>>>> origin/daddy
