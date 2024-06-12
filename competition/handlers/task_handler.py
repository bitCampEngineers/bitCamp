from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    title: str
    link: str
    difficulty: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    competitions: Optional[List[int]] = []
    cases: Optional[List[int]] = []

    class Config:
        orm_mode = True
