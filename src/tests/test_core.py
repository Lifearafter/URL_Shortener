from urllib import response
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import sys

from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
from os import environ, path

if __package__:
    parent_dir = path.dirname(__file__)
    path_two = "c:\\Zaid\\Fun Projects -- Code\\URL_Shortener\\src\\api"
    path = path.dirname(path_one)
    path2 = path.dirname(path_two)
    if path not in sys.path:
        sys.path.append(path)
    if path_one not in sys.path:
        sys.path.append(path_one)
from ..api.api import app, get_db

load_dotenv()

user = environ.get("DB_USER_TEST")
password = environ.get("DB_PASSWORD_TEST")
port = environ.get("DB_PORT_TEST")
ip = environ.get("DB_IP_TEST")

client = TestClient(app)

engine = create_engine(
    "mysql:pymysql://{user}:{password}@{ip}:{port}/testurldb".format(
        user=user, password=password, ip=ip, port=port
    )
)
Session = sessionmaker(bind=engine)


async def overrideDB():
    db = Session()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = overrideDB


def add_url():
    response = client.post("/add?longurl=https://google.com")
    currtime = datetime.now.strftime("%Y-%m-%d")
    assert response.status_code == 200
    assert response.json == {
        "short_url": "0",
        "long_url": "https://google.com",
        "time": "{timenow}".format(timenow=currtime),
    }
    response = client.post("/add?longurl=www.google.com")
    assert response.status_code == 200
    assert response.json == {
        "short_url": "1",
        "long_url": "www.google.com",
        "time": "{timenow}".format(timenow=currtime),
    }


def find_short_url():
    response = client.get("/url?longurl=https://google.com")
    assert response.status_code == 200
    assert response.json == {
        "short_url": "0",
        "long_url": "https://google.com",
        "time": "2022-07-26",
    }
    response = client.get("/url?longurl=www.google.com")
    assert response.status_code == 200
    assert response.json == {
        "short_url": "1",
        "long_url": "www.google.com",
        "time": "2022-07-26",
    }
    response = client.get("/url?longurl=https://assawdsawsawaasa.com")
    assert response.status_code == 404
    assert response.json == {"status": "404", "message": "Not found"}


def redirect():
    response = client.get("/0")
    assert response.status_code == 301
