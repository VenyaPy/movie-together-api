from fastapi import FastAPI
from app.models.users.router import router_user, router_auth
from app.models.search.router import router_search

app = FastAPI(
    title="Совместный просмотр фильмов",
    version="0.1.0",
)


app.include_router(router_user)
app.include_router(router_auth)
app.include_router(router_search)

