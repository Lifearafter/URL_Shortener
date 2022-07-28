from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from ..api import app
from ..db.dbmng import DBMng

from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
from os import environ

load_dotenv()

user = environ.get("DB_USER_TEST")
password = environ.get("DB_PASSWORD_TEST")
port = environ.get("DB_PORT_TEST")
ip = environ.get("DB_IP_TEST")

client = TestClient(app)

url = "mysql:pymysql://{user}:{password}@{ip}:{port}/testurldb".format(
    user=user, password=password, ip=ip, port=port
)
engine = create_engine(url)
Session = sessionmaker(bind=engine)


def find_short_url():
    response = client.get("/url?longurl=https://google.com")
    assert response.status_code == 200
    assert response.json == {
        "short_url": "0",
        "long_url": "www.google.com",
        "time": "2022-07-26",
    }
    response = client.get("/url?longurl=google.com")
    assert response.status_code == 200
    assert response.json == {
        "short_url": "0",
        "long_url": "www.google.com",
        "time": "2022-07-26",
    }
    response = client.get("/url?longurl=https://assawdsawsawaasa.com")
    assert response.status_code == 404
    assert response.json == {"status": "404", "message": "Not found"}


def redirect():
    response = client.get("/0")
    assert response.status_code == 301
