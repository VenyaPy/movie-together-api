from pydantic import BaseModel
from datetime import datetime


class Room(BaseModel):
    id: int
    room_id: str
    movie_url: str
    username: str
    time: datetime

    class Config:
        orm_mode = True