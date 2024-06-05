from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base


class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    input_id = Column(Integer, ForeignKey('input.id'))
    output = Column(String)
    input_type = Column(String)
    output_type = Column(String)


    # Many-to-One relationship with Task
    task = relationship('Task', back_populates='cases')


    # Many-to-One relationship with Input
    input = relationship('Input')