from typing import Any, Dict, List, NewType, Type, Union
from fastapi import FastAPI

from .feed_reader import get_rss_feed, TemporaryFeed
app = FastAPI()


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/feed/{rss_source}")
def get_feed(rss_source: str) -> TemporaryFeed:
    if result := get_rss_feed(rss_source):
        return result
    return NotImplementedError
