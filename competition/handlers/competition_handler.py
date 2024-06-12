from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CompetitionBase(BaseModel):
    task_id: int
    start_time: datetime
    end_time: datetime
    is_active: bool

class CompetitionCreate(CompetitionBase):
    pass

class Competition(CompetitionBase):
    id: int
    users: Optional[List[int]] = []

    class Config:
        orm_mode = True
