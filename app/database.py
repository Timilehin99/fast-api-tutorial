from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = "postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"


try:
    conn = psycopg2.connect(host = 'localhost', dbname = 'fastapiV1', user = 'postgres',
    password = 'timi', cursor_factory = RealDictCursor)

    cursor = conn.cursor()

    print('............. .\n Connection sucessful \n .............')

except Exception as error:
    print(error)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()