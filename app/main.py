from datetime import datetime, timedelta
from random import shuffle
from typing import Callable, List

from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse

from .models import create_db
from .schemas import Log
from .utilities import add_log, get_latest_log

app = FastAPI(title="Glia Technical Assessment API")
create_db()


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Hello Glia"


@app.get(
    "/jumble/{word}",
    summary="Randomly rearrange the characters of a word",
    response_class=PlainTextResponse,
)
async def jumble(word: str):
    chars = list(word)
    shuffle(chars)
    jumbled = "".join(chars)
    return jumbled


@app.get(
    "/audit",
    summary="Return the last n requests made to the application",
    response_model=List[Log],
)
async def audit(n: int = 10):
    return [Log.from_orm(db_log) for db_log in get_latest_log(n)]


@app.middleware("http")
async def request_middleware(request: Request, call_next: Callable):
    start_time = datetime.now()
    response = await call_next(request)
    end_time = datetime.now()

    ms = timedelta(milliseconds=1)
    add_log(
        date=start_time,
        url=str(request.url),
        path=request.url.path,
        status=response.status_code,
        duration_ms=(end_time - start_time) / ms,
    )
    return response
