import os

from dotenv import load_dotenv

load_dotenv()


class DBCreds:
    HOST = os.environ["DB_HOST"]
    PORT = os.environ["DB_PORT"]
    DBNAME = os.environ["DB_NAME"]
    USER = os.environ["DB_USER"]
    PASSWORD = os.environ["DB_PASSWORD"]
