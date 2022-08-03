from fastapi.testclient import TestClient

from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from datetime import datetime

from dotenv import load_dotenv
from os import environ, path
import sys

# if __package__:
parent_dir = path.dirname(__file__)
root_dir = path.dirname(parent_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)
from api.api import app, get_db

load_dotenv()

user = environ.get("DB_USER_TEST")
password = environ.get("DB_PASSWORD_TEST")
port = environ.get("DB_PORT_TEST")
ip = environ.get("DB_IP_TEST")

engine = create_engine(
    "mysql+pymysql://{user}:{password}@{ip}:{port}/testurldb".format(
        user=user, password=password, ip=ip, port=port
    )
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class URL(Base):
    __tablename__ = "urls"

    short_url = Column(String(256), primary_key=True, unique=True, nullable=False)
    long_url = Column(String(768), nullable=False, unique=True)
    time = Column(String(256), nullable=False)

    def __init__(self, short_url, long_url, time):
        self.short_url = short_url
        self.long_url = long_url
        self.time = time


class Users(Base):
    __tablename__ = "users"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    user_type = Column(Boolean, nullable=False)
    auth_key = Column(String(256), unique=True)

    def __init__(self, user_type, auth_key):
        self.user_type = user_type
        self.auth_key = auth_key


Base.metadata.create_all(bind=engine)


def overrideDB():
    db = Session()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = overrideDB

client = TestClient(app)


def test_add_url():
    response = client.post("/add?long_url=https://google.com")
    currtime = datetime.now().strftime("%Y-%m-%d")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://google.com"
    assert data["short_url"] == "0"
    assert data["time"] == currtime
    response = client.post("/add?long_url=www.google.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "www.google.com"
    assert data["short_url"] == "1"
    assert data["time"] == currtime


def test_find_short_url():
    response = client.get("/url?long_url=https://google.com")
    currtime = datetime.now().strftime("%Y-%m-%d")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://google.com"
    assert data["short_url"] == "0"
    assert data["time"] == currtime

    response = client.get("/url?long_url=www.google.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "www.google.com"
    assert data["short_url"] == "1"
    assert data["time"] == currtime

    response = client.get("/url?long_url=https://assawdsawsawaasa.com")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "404"
    assert data["message"] == "Not found"


def test_redirect():
    response = client.get("/0")
    assert response.status_code == 307


test_redirect()


def test_delete():
    currtime = datetime.now().strftime("%Y-%m-%d")

    response = client.delete("/delete?long_url=https://google.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://google.com"
    assert data["short_url"] == "0"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=www.google.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "www.google.com"
    assert data["short_url"] == "1"
    assert data["time"] == currtime
