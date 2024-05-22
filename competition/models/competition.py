from sqlalchemy import Boolean, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.db import Base
from shared.models import user_competition_tb



class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_active = Column(Boolean)
    
    
    users = relationship("User", secondary=user_competition_tb, back_populates="competitions")
    tasks = relationship("Task", back_populates="competitions")