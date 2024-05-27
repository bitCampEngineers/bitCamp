from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from .models import models
import datetime

"""This all handlers are not ready to use at all"""
class CompetitionBase(BaseModel):
    task: str


class CompetitionCreate(CompetitionBase):
    pass

class Competition(CompetitionBase):
    id: int
    start_time: datetime
    end_time: datetime

    class Config:
        orm_mode = True

class CompetitionParticipantBase(BaseModel):
    completion_time: datetime
    result: int

class CompetitionParticipantCreate(CompetitionParticipantBase):
    competition_id: int
    user_id: int

class CompetitionParticipant(CompetitionParticipantBase):
    id: int
    competition_id: int
    user_id: int

    class Config:
        orm_mode = True


def get_leetcode_task():
    pass