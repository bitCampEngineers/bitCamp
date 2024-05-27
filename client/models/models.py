from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base
from shared.models import user_competition_tb


class User(Base):
    __tablename__  = "users"


    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    points = Column(Integer)
    is_active = Column(Boolean, default=True)
    solved_tasks = Column(String)

    competitions = relationship("Competition", secondary=user_competition_tb, back_populates="users")