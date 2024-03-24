from app.dao.dao import BaseDAO
from app.models.session.model import Session


class RoomDAO(BaseDAO):
    model = Session