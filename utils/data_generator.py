from faker import Faker

fake = Faker("ru_RU")


class DataGenerator:
    """генератор тестовых данных для фильмов"""

    @staticmethod
    def generate_movie_data(genre_id, location="MSK", published=True):
        """генерирует валидный словарь данных для создание фльима"""

        return {
            "name": f"Movie {fake.uuid4()}",
            "price": fake.random_int(min=100, max=1000),
            "description": fake.text(max_nb_chars=200),
            "location": location,
            "published": published,
            "genreId": genre_id,
            "imageUrl": fake.image_url()
        }
