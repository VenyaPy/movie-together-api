from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.database import Base

user_session_table = Table('user_session', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True)
)