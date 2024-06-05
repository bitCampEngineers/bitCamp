from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from config.db import Base



class Input(Base):
    __tablename__ = 'input'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    value = Column(String)