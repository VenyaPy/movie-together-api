from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.search.schemas import Movie
from app.models.search.hbtv import fetch_movies


router_search = APIRouter(
    prefix="/search",
    tags=["Поиск фильмов"],
)


@router_search.post("/{search_name}", response_model=List[Movie])
async def search_film(search_name: str) -> List[Movie]:
    movies_data = await fetch_movies(search_name)
    if not movies_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Фильмы не найдены")
    movies = [Movie(**movie) for movie in movies_data]
    return movies
