from fastapi import APIRouter, HTTPException, status

from app.apiconnect.apivb import popular_films
from app.models.mainpage.schemas import PopularFilms
from typing import List


main_router = APIRouter(
    tags=["Главная страница"]
)


@main_router.get("/mainpage", response_model=List[PopularFilms])
async def main_page():
    movies_data = await popular_films()
    if not movies_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдено")

    return movies_data
