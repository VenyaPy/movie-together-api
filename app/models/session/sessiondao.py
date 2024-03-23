from app.dao.dao import BaseDAO
from app.models.session.model import Session  # Импортируйте вашу модель Session


class SessionDAO(BaseDAO):
    model = Session
