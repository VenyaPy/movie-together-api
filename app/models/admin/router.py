from typing import Optional

from sqladmin import ModelView
from app.models.users.model import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.username, Users.email, Users.status, Users.date, Users.image]
    name = "Пользователь"
    name_plural = "Пользователи"
