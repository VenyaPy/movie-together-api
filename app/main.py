from fastapi import FastAPI

app = FastAPI(
    title="Совместный просмотр фильмов",
    version="0.1.0",
    root_path="/api",
)

