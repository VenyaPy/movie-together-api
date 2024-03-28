from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.models.search.schemas import Movie, RandomMovie
from app.apiconnect.apivb import fetch_movies, random_films
from app.models.users.dependencies import get_current_user
from app.models.users.model import Users



router_search = APIRouter(
    prefix="/search",
    tags=["Поиск фильмов"],
)


@router_search.post("/{name}")
async def search_film(
        name: str,
        current_user: Users = Depends(get_current_user)
) -> List[Movie]:

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не авторизованы"
        )

    movies_data = await fetch_movies(name)
    if not movies_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Фильмы не найдены")

    movies = [Movie(**movie) for movie in movies_data]
    return movies


@router_search.get("/random", response_model=RandomMovie)
async def search_popular(current_user: Users = Depends(get_current_user)):

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не авторизованы"
        )

    movie_data = await random_films()
    if not movie_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неудачный запрос")

    return movie_data
