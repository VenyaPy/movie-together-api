from app.dao.dao import BaseDAO
from app.models.users.model import Users


class UserDAO(BaseDAO):
    try:
        model = Users
    except Exception as e:
        print(e)