from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class GenreModel(BaseModel):
    """Модель жанра, вложенного в ответ фильма.

    id оставлен опциональным намеренно: по Swagger-схеме (GenreResponse) поле id
    обязательное, но фактический ответ дев-стенда на всех проверенных эндпоинтах
    (GET /movies, POST /movies, GET /movies/{id}) содержит только {"name": "..."}
    без id. Если бэкенд когда-нибудь начнёт отдавать id, эта модель это переживёт,
    но остаётся расхождение со Swagger, о котором стоит сообщить бэкенд-команде.
    """

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
    rating: float
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
