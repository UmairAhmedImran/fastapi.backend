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

#creating a connection to database, use this when you want to use raw SQL and not sqlalchemy
# while True:
#     try:
#         conn = psycopg2.connect(host= 'localhost', database='fastapi', user = 'postgres', password = '857LOVE$$#u', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was sucessfull")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print("Error", error)
#         time.sleep(2)
