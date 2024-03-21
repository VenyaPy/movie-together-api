from fastapi import FastAPI
from sqladmin import Admin

from app.database.database import engine
from app.models.admin.router import UserAdmin
from app.models.users.router import router_user, router_auth
from app.models.search.router import router_search
from app.models.admin.auth import auth_backend


app = FastAPI(
    title="Совместный просмотр фильмов",
    version="0.1.0",
)

admin = Admin(app, engine, authentication_backend=auth_backend)


app.include_router(router_user)
app.include_router(router_auth)
app.include_router(router_search)

admin.add_view(UserAdmin)

