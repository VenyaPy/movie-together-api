from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.models.search.schemas import Movie
from app.models.search.apivb import fetch_movies
from app.models.users.dependencies import get_current_user
from app.models.users.model import Users


router_search = APIRouter(
    prefix="/search",
    tags=["Поиск фильмов"],
)


@router_search.post("/{name}", response_model=List[Movie])
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
