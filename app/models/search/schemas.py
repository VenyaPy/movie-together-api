from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class Movie(BaseModel):
    title_ru: str
    title_en: str
    year: int
    kinopoisk_id: int
    type: str
    iframe_url: HttpUrl
    block: bool
    quality: str
    poster: HttpUrl
    trailer: str | None
