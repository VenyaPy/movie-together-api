from app.database.database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    movie_id = Column(String)
    time = Column(DateTime, nullable=False)
