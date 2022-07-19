from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:1itedc23@localhost:3306/sqlalchemy")

Session = sessionmaker(bind=engine)

Base = declarative_base()
