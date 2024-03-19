from app.database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship




class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    movie_id = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
