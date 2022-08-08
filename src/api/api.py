from cgitb import handler
from string import ascii_letters, digits
from mangum import Mangum

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, Query, Path
from pydantic import BaseModel
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import datetime

import sys
import os

if __package__:
    parentdir = os.path.dirname(__file__)
    rootdir = os.path.dirname(parentdir)
    if rootdir not in sys.path:
        sys.path.append(rootdir)
    if parentdir not in sys.path:
        sys.path.append(parentdir)

from db.base import engine, SessionLocal, Base
from db.url import URL
from db.users import Users
from db import dbmng

origins = ["http://127.0.0.1:5500/docs/"]

tags_metadata = [
    {
        "name": "Non-Authenticated",
        "description": "API endpoints that do not require authentication.",
    },
    {
        "name": "Authenticated",
        "description": "API endpoints that require authentication.",
    },
]

Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_tags=tags_metadata, root_path="/dev")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class URL(BaseModel):
    long_url: str
    short_url: str
    time: str

    class Config:
        schema_extra = {
            "example": {
                "long_url": "https://www.google.com",
                "short_url": "h129nu1i",
                "time": "2020-01-01",
            }
        }
        orm_mode = True


responses = {
    400: {
        "content": {
            "application/json": {
                "example": {
                    "status": "400",
                    "message": "Bad request",
                }
            }
        }
    },
    404: {
        "content": {
            "application/json": {
                "example": {
                    "status": "404",
                    "message": "Not found",
                }
            }
        }
    },
    500: {
        "content": {
            "application/json": {
                "example": {
                    "status": "500",
                    "message": "Server Error. Server could be down for maintainance",
                }
            }
        }
    },
}


async def shorten(last_char: str):
    letters = ascii_letters
    digit = digits
    isNextChar = False
    addedchar: str

    if last_char in digit:
        if last_char != "9":
            for y in digit:
                if y == last_char:
                    addedchar = digit[digit.index(y) + 1]
                    isNextChar = True
                    break
        else:
            addedchar = "a"
    elif last_char in ascii_letters:
        if last_char != "Z":
            for x in letters:
                if x is last_char:
                    addedchar = letters[letters.index(x) + 1]
                    break
        else:
            addedchar = "0"
            isNextChar = True

    return addedchar


def checkurl(url: str) -> bool:
    if url.startswith("http://") or url.startswith("https://"):
        return True
    else:
        return False


def addscheme(url: str):
    return "http://" + url


def stripurl(url: str):
    if url.startswith("http://"):
        url = url.replace("http://", "")
        return url
    elif url.startswith("https://"):
        url = url.replace("https://", "")
        return url
    else:
        return url


@app.get(
    "/url",
    response_model=URL,
    tags=["Non-Authenticated"],
    responses={**responses},
)
async def find_Short_URL(
    longurl: str = Query(
        default=...,
        max_length=256,
        description="long URL associated with short URL",
        alias="long_url",
    ),
    db: Session = Depends(get_db),
):
    stripped = stripurl(longurl)

    dbmodel = dbmng.find_short_url(db, stripped)
    if dbmodel != None:
        model = URL.from_orm(dbmodel)
        model.long_url = longurl
        return model
    else:
        return JSONResponse(
            status_code=404, content={"status": "404", "message": "Not found"}
        )


@app.get(
    "/{short_url}",
    response_class=RedirectResponse,
    tags=["Non-Authenticated"],
    responses={**responses},
)
async def redirect(
    short_url: str = Path(default=..., description="short URL to redirect"),
    db: Session = Depends(get_db),
):
    dbmodel = dbmng.get_short_url(db, short_url)
    if dbmodel != None:
        model = URL.from_orm(dbmodel)
        url = addscheme(model.long_url)
        return RedirectResponse(url)
    else:
        return JSONResponse(
            status_code=404, content={"status": "404", "message": "Not found"}
        )


@app.post(
    "/add",
    response_model=URL,
    tags=["Non-Authenticated"],
    responses={**responses},
)
async def add_url(
    long_url: str = Query(
        max_length=2043,
        description="URL to shorten",
        alias="long_url",
    ),
    db: Session = Depends(get_db),
):
    stripped = stripurl(long_url)
    dbmodel = dbmng.get_last_entry(db)

    if dbmodel != None:
        shortUrl = await shorten(dbmodel.short_url)
        model = URL(
            short_url=shortUrl,
            long_url=stripped,
            time=datetime.now().strftime("%Y-%m-%d"),
        )
        x = dbmng.insert_url(db, model.short_url, model.long_url, model.time)
        if x is None:
            mod = dbmng.find_short_url(db, stripped)
            url = URL.from_orm(mod)
            url.long_url = long_url
            return url
        url = URL.from_orm(x)
        url.long_url = long_url
        return url
    else:
        shortUrl = "0"
        model = URL(
            short_url=shortUrl,
            long_url=stripped,
            time=datetime.now().strftime("%Y-%m-%d"),
        )
        x = dbmng.insert_url(db, model.short_url, model.long_url, model.time)
        url = URL.from_orm(x)
        url.long_url = long_url
        return url


@app.delete(
    "/delete",
    tags=["Authenticated"],
    response_model=URL,
    responses={
        **responses,
        401: {"401": {"description": "Unauthorized"}},
    },
)
async def delete(
    long_url: str = Query(default=..., description="long URL to delete"),
    db: Session = Depends(get_db),
):
    check_url = checkurl(long_url)
    if check_url:
        stripped = stripurl(long_url)
        dbmodel = dbmng.find_short_url(db, stripped)
    else:
        dbmodel = dbmng.find_short_url(db, long_url)

    if dbmodel != None:
        url = URL.from_orm(dbmodel)
        dbmng.drop_url(db, dbmodel.short_url)
        url.long_url = long_url
        return url
    else:
        return JSONResponse(
            status_code=404, content={"status": "404", "message": "Not found"}
        )


handler = Mangum(app=app)
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
