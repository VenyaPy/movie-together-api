from fastapi import FastAPI
from app.models.users.router import router_user, router_auth

app = FastAPI(
    title="Совместный просмотр фильмов",
    version="0.1.0",
    root_path="/api",
)


app.include_router(router_user)
app.include_router(router_auth)

