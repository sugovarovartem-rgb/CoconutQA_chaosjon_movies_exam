from typing import Optional

from db_models.db_session import SessionLocal
from db_models.movies import MovieDBModel


def get_movie_by_id_from_db(movie_id: int) -> Optional[MovieDBModel]:
    """Возвращает фильм из БД по id или None, если фильм отсутствует."""

    session = SessionLocal()
    try:
        return session.get(MovieDBModel, movie_id)
    finally:
        session.close()


def get_movie_by_name_from_db(name: str) -> Optional[MovieDBModel]:
    """Возвращает фильм из БД по имени или None, если фильм отсутствует."""

    session = SessionLocal()
    try:
        return session.query(MovieDBModel).filter(MovieDBModel.name == name).first()
    finally:
        session.close()
