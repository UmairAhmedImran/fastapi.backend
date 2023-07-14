from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2 # to connect DB
from psycopg2.extras import RealDictCursor # to have column of the table
from .config import Settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{Settings.database_username}:{Settings.database_password}@{Settings.database_hostname}:{Settings.database_port}/{Settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Sessionlocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


