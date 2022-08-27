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

user = environ.get("DB_USER")
password = environ.get("DB_PASSWORD")
port = environ.get("DB_PORT")
ip = environ.get("DB_IP")

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

    response = client.post("/add?long_url=https://www.facebook.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.facebook.com"
    assert data["short_url"] == "2"
    assert data["time"] == currtime

    response = client.post("/add?long_url=https://stackoverflow.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://stackoverflow.com"
    assert data["short_url"] == "3"
    assert data["time"] == currtime

    response = client.post("/add?long_url=https://www.youtube.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.youtube.com"
    assert data["short_url"] == "4"
    assert data["time"] == currtime

    response = client.post("/add?long_url=https://www.utdallas.edu/galaxy")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.utdallas.edu/galaxy"
    assert data["short_url"] == "5"
    assert data["time"] == currtime

    response = client.post("/add?long_url=https://www.lttstore.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.lttstore.com"
    assert data["short_url"] == "6"
    assert data["time"] == currtime

    response = client.post("/add?long_url=https://www.amazon.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.amazon.com"
    assert data["short_url"] == "7"
    assert data["time"] == currtime

    response = client.post("/add?long_url=https://github.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://github.com"
    assert data["short_url"] == "8"
    assert data["time"] == currtime

    response = client.post(
        "/add?long_url=http://lifearafter.github.io/Personal_Website"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "http://lifearafter.github.io/Personal_Website"
    assert data["short_url"] == "9"
    assert data["time"] == currtime

    response = client.post("/add?long_url=https://resumeworded.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://resumeworded.com"
    assert data["short_url"] == "a"
    assert data["time"] == currtime

    response = client.post("/add?long_url=https://github.com/Lifearafter")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://github.com/Lifearafter"
    assert data["short_url"] == "b"
    assert data["time"] == currtime

    response = client.post("/add?long_url=https://github.com/Lifearafter")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://github.com/Lifearafter"
    assert data["short_url"] == "b"
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
    assert response.url == "http://google.com"
    response = client.get("/1")
    assert response.url == "http://www.google.com"

    response = client.get("/Z")
    data = response.json()
    assert data["status"] == "404"
    assert data["message"] == "Not found"


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

    response = client.delete("/delete?long_url=https://www.facebook.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.facebook.com"
    assert data["short_url"] == "2"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=https://stackoverflow.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://stackoverflow.com"
    assert data["short_url"] == "3"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=https://www.youtube.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.youtube.com"
    assert data["short_url"] == "4"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=https://www.utdallas.edu/galaxy")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.utdallas.edu/galaxy"
    assert data["short_url"] == "5"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=https://www.lttstore.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.lttstore.com"
    assert data["short_url"] == "6"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=https://www.amazon.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://www.amazon.com"
    assert data["short_url"] == "7"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=https://github.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://github.com"
    assert data["short_url"] == "8"
    assert data["time"] == currtime

    response = client.delete(
        "/delete?long_url=https://lifearafter.github.io/Personal_Website"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://lifearafter.github.io/Personal_Website"
    assert data["short_url"] == "9"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=https://resumeworded.com")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://resumeworded.com"
    assert data["short_url"] == "a"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=https://github.com/Lifearafter")
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://github.com/Lifearafter"
    assert data["short_url"] == "b"
    assert data["time"] == currtime

    response = client.delete("/delete?long_url=https://www.linkedin.com/in/lifearafter")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "404"
    assert data["message"] == "Not found"
