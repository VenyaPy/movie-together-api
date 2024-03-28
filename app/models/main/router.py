from fastapi import APIRouter, HTTPException, status

from app.models.search.apivb import popular_films


main_router = APIRouter(
    tags=["Главная страница"]
)


@main_router.get("/")
async def main_page():
    movie = await popular_films()
    if not movie:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдено")

    return movie