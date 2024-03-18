from app.database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.user_session_table.session_table import user_session_table



class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    movie_id = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    users = relationship("Users", secondary=user_session_table, back_populates="sessions")
