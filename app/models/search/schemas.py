from pydantic import BaseModel, HttpUrl, validator
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


class RandomMovie(BaseModel):
    id: str
    type: str
    name: str
    description: str
    year: int
    poster: HttpUrl
    trailer_url: HttpUrl

    @validator('poster', pre=True)
    def url_poster(cls, v):
        return v['url']




