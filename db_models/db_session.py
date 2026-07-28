from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from resources.db_creds import DBCreds

DB_URL = (
    f"postgresql+psycopg2://{DBCreds.USER}:{DBCreds.PASSWORD}"
    f"@{DBCreds.HOST}:{DBCreds.PORT}/{DBCreds.DBNAME}"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
