from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import sys

from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
from os import environ, path

# if __package__:
parent_dir = path.dirname(__file__)
root_dir = path.dirname(parent_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)
from api.api import app, get_db
from api.db.base import Base

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
    response = client.post("/add?longurl=https://google.com")
    currtime = datetime.now().strftime("%Y-%m-%d")
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


def test_find_short_url():
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


def test_redirect():
    response = client.get("/0")
    assert response.status_code == 301
