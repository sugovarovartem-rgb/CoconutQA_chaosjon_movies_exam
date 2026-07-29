from faker import Faker

fake = Faker("ru_RU")


class DataGenerator:
    """генератор тестовых данных для фильмов"""

    @staticmethod
    def generate_movie_data(genre_id, location="MSK", published=True):
        """генерирует валидный словарь данных для создание фильма"""

        return {
            "name": f"Movie {fake.uuid4()}",
            "price": fake.random_int(min=100, max=1000),
            "description": fake.text(max_nb_chars=200),
            "location": location,
            "published": published,
            "genreId": genre_id,
            "imageUrl": fake.image_url()
        }

    @staticmethod
    def generate_random_email():
        """Генерирует уникальный email"""
        return f"test_{fake.uuid4()}@gmail.com"

    @staticmethod
    def generate_random_name():
        """Генерирует случайное полное имя"""
        first_name = fake.first_name()
        last_name = fake.last_name()
        return f"{first_name} {last_name}"

    @staticmethod
    def generate_random_password():
        """Генерирует пароль, подходящий требованиям сервиса"""
        return f"Test{fake.random_int(min=1000, max=9999)}@"
