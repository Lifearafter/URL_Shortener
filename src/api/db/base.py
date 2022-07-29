from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import environ

load_dotenv()

root = environ.get("DB_USER")
password = environ.get("DB_PASSWORD")
port = environ.get("DB_PORT")
ip = environ.get("DB_IP")


engine = create_engine(
    "mysql+pymysql://{root}:{password}@{ip}:{port}/urldb".format(
        root=root, password=password, ip=ip, port=port
    )
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
