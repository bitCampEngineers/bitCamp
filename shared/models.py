from sqlalchemy import Table, Column, Integer, ForeignKey
from config.db import Base 

user_competition_tb = Table(
    'user_competition',
    Base.metadata,
    Column("competition_id", Integer, ForeignKey("competitions.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)