from typing import Dict
from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from news_feed.feed_reader import get_rss_feed, TemporaryFeed


app = FastAPI()


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/feed/{rss_source}")
def get_feed(rss_source: str, skip: int = 0, limit: int = 20) -> TemporaryFeed:
    try:
        if result := get_rss_feed(rss_source, skip=skip, limit=limit):
            return result
    except AssertionError as msg:
        raise HTTPException(status_code=400, detail=f'{msg}')

    except NotImplementedError as err:
        raise HTTPException(status_code=400, detail=f'{rss_source} is not an available feed source')
    else:
        raise HTTPException(status_code=400, detail='Unknown request')
