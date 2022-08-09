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
import re

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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
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
                    break
        else:
            addedchar = "a"
    elif last_char in ascii_letters:
        if last_char != "z":
            for x in letters:
                if x is last_char:
                    addedchar = letters[letters.index(x) + 1]
                    break
        else:
            addedchar = "0"
            isNextChar = True

    return (addedchar, isNextChar)


def is_url(url: str) -> bool:
    regex = r'/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g'
    return re.match(regex, url) is not None


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

    dbmodel = dbmng.find_url_given_long(db, stripped)
    if dbmodel is not None:
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
    if dbmodel is not None:
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
    last_entry = dbmng.get_last_entry(db)

    # if URL is mapped in DB already
    if last_entry is not None:
        urlPath = hex(int(last_entry.short_url, base=16) - 1)
        shortUrl = f"{urlPath.zfill(len(urlPath))}"
        model = URL(
            short_url=shortUrl,
            long_url=stripped,
            time=datetime.now().strftime("%Y-%m-%d"),
        )
        stored_url = dbmng.insert_url(db, model)
        if stored_url is None:
            mod = dbmng.find_url_given_long(db, stripped)
            url = URL.from_orm(mod)
            url.long_url = long_url
            return url
        url = URL.from_orm(stored_url)
        url.long_url = long_url
        return url
    # if no URL is mapped in DB already- we need to add the first one
    else:
        # first 1000 digits of pi
        shortUrl = "1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989"
        model = URL(
            short_url=shortUrl,
            long_url=stripped,
            time=datetime.now().strftime("%Y-%m-%d"),
        )
        stored_url = dbmng.insert_url(db, model)
        url = URL.from_orm(stored_url)
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
    is_url = is_url(long_url)
    if is_url:
        stripped = stripurl(long_url)
        dbmodel = dbmng.find_url_given_long(db, stripped)
    else:
        dbmodel = dbmng.find_url_given_long(db, long_url)

    if dbmodel is not None:
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
