from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class GenreModel(BaseModel):
    """Модель жанра, вложенного в ответ фильма."""

    model_config = ConfigDict(extra="allow")

    name: str
    id: Optional[int] = None


class MovieResponseModel(BaseModel):
    """Модель одного фильма в ответе Movies API (POST /movies, GET /movies/{id})."""

    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    price: int
    description: str
    imageUrl: str
    location: str
    published: bool
    rating: Optional[float] = None
    genreId: int
    createdAt: str
    genre: Optional[GenreModel] = None
    reviews: Optional[list[Any]] = None


class MoviesListResponseModel(BaseModel):
    """Модель ответа GET /movies - список фильмов с пагинацией."""

    model_config = ConfigDict(extra="allow")

    movies: list[MovieResponseModel]
    count: int
    page: int
    pageSize: int
    pageCount: int
