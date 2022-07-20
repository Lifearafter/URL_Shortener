from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import environ

load_dotenv()

root = environ.get("DB_ROOT")
password = environ.get("DB_PASSWORD")
port = environ.get("DB_PORT")


engine = create_engine("mysql+pymysql://{root}:{password}@{port}/sqlalchemy")

Session = sessionmaker(bind=engine)

Base = declarative_base()
