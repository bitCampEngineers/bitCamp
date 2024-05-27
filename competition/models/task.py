from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from config.db import Base



class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    link = Column(String)
    difficulty = Column(String)

    competitions = relationship("Competition", back_populates="tasks")