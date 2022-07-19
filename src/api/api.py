from string import ascii_letters, digits
import uvicorn

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from datetime import datetime


class URL(BaseModel):
    long_url: str
    short_url: str | None = None  # Change when finished with db
    time: str

    class Config:
        schema_extra = {
            "example": {
                "long_url": "https://www.google.com",
                "short_url": "h129nu1i",
                "time": "2020-01-01",
            }
        }


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

app = FastAPI(openapi_tags=tags_metadata)


async def shorten(last_char: str):
    letters = ascii_letters
    digit = digits
    isNextChar = False
    addedchar: str

    if last_char in digit:
        if last_char != "9":
            for y in digit:
                addedchar = digit[digit.index(x) + 1]
        else:
            addedchar = "a"
    elif last_char in ascii_letters:
        if last_char != "Z":
            for x in letters:
                if x is last_char:
                    addedchar = letters[letters.index(x) + 1]
        else:
            addedchar = "0"
            isNextChar = True

    return addedchar, isNextChar


@app.get(
    "/url",
    response_model=URL,
    tags=["Non-Authenticated"],
    responses={**responses},
)
async def find_Short_URL(
    longURL: str = Query(
        default=...,
        max_length=2043,
        description="long URL associated with short URL",
        alias="long url",
    ),
):
    model: URL = URL(long_url=longURL, time=datetime.now().strftime("%Y-%m-%d"))
    return model


@app.get(
    "/{short_url}",
    response_class=RedirectResponse,
    tags=["Non-Authenticated"],
    responses={**responses, 307: {"307": {"description": "Redirect to long URL"}}},
)
async def redirect(
    short_url: str = Path(default=..., description="short URL to redirect")
):
    return RedirectResponse(short_url)


@app.post(
    "/add/{long_url}",
    response_model=URL,
    tags=["Authenticated"],
    responses={
        **responses,
        200: {"200": {"description": "Success"}},
        401: {"401": {"description": "Unauthorized"}},
    },
)
async def add_url(
    long_url: str = Path(
        max_length=2043,
        description="URL to shorten",
        alias="long url",
    ),
):
    shortUrl = await shorten(long_url)
    model: URL = URL(
        long_url=long_url,
        short_url=shortUrl,
        time=datetime.now().strftime("%Y-%m-%d"),
    )

    return model


@app.delete(
    "/{long_url}",
    tags=["Authenticated"],
    response_model=URL,
    responses={
        **responses,
        204: {"200": {"description": "URL Deleted"}},
        401: {"401": {"description": "Unauthorized"}},
    },
)
async def delete(long_url: str = Path(default=None, description="long URL to delete")):
    model: URL = URL(long_url=long_url, time=datetime.now().strftime("%Y-%m-%d"))
    return model


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
