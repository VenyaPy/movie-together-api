from fastapi import FastAPI
from sqladmin import Admin

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from app.database.database import engine
from app.models.admin.router import UserAdmin
from app.models.users.router import router_user, router_auth
from app.models.search.router import router_search
from app.models.admin.auth import auth_backend
from app.models.rooms.router import room_router
from app.models.images.router import image_router
from app.models.mainpage.router import main_router


app = FastAPI(
    title="Совместный просмотр фильмов",
    version="0.1.0",
)


admin = Admin(app, engine, authentication_backend=auth_backend)

app.include_router(main_router)
app.include_router(router_user)
app.include_router(router_auth)
app.include_router(image_router)
app.include_router(router_search)
app.include_router(room_router)

admin.add_view(UserAdmin)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url("redis://localhost ")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
