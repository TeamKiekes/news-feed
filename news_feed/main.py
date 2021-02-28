from typing import Dict, Any, List, Optional
from fastapi import FastAPI

from .feed_reader import get_rss_feed
app = FastAPI()


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/feed/{rss_source}")
def get_feed(rss_source: str) -> Optional[List[Dict[str, Any]]]:
    if result := get_rss_feed(rss_source):
        return result
    return None
