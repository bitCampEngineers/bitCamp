from pydantic import BaseModel
from typing import Optional

class CaseBase(BaseModel):
    task_id: int
    input_id: int
    output: str
    input_type: str
    output_type: str

class CaseCreate(CaseBase):
    pass

class Case(CaseBase):
    id: int

    class Config:
        orm_mode = True



