import psycopg2

from resources.db_creds import DBCreds


def connect_to_movies_db():
    """Подключается к БД Movies и выводит информацию о PostgreSQL сервере."""

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            dbname=DBCreds.DBNAME,
            user=DBCreds.USER,
            password=DBCreds.PASSWORD,
            host=DBCreds.HOST,
            port=DBCreds.PORT,
        )
        cursor = connection.cursor()

        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL version: {version[0]}")

    except Exception as error:
        print(f"Ошибка при подключении к PostgreSQL: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    connect_to_movies_db()
