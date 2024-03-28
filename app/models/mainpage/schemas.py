from pydantic import BaseModel, HttpUrl, validator


class PopularFilms(BaseModel):
    id: str
    type: str
    name: str
    description: str
    year: int
    poster: HttpUrl


    @validator('poster', pre=True)
    def url_poster(cls, v):
        return v['url']