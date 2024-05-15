from sqlalchemy import Boolean,Column,Integer,String
from config.db import Base


class User(Base):
    __tablename__  = "users"


    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    point = Column(Integer)
    is_active = Column(Boolean=True)