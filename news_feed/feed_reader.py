
from typing import Any, Dict, List, NewType, Type, Union
import feedparser  # type: ignore


VRT_RSS_URL = 'https://www.vrt.be/vrtnieuws/en.rss.articles.xml'
VRT_RSS_FILE = './tests/resources/en.rss.articles.xml'

Feed = NewType('Feed', List[Dict[str, Any]])
TemporaryFeed = Union[Type[NotImplementedError], Feed]


def get_rss_feed(source: str) -> TemporaryFeed:
    if source == 'vrt':
        return get_vrt_feed()
    return NotImplementedError


def get_vrt_feed() -> Feed:
    testing = True
    rss_location = VRT_RSS_URL
    if testing:
        rss_location = VRT_RSS_FILE

    d = feedparser.parse(rss_location)
    print(d.keys())
    print(d.feed.keys())
    # ['language', 'title', 'title_detail', 'logo', 'id', 'guidislink', 'link', 'updated', 'updated_parsed', 'authors', 'author_detail', 'author', 'links']
    entries: Feed = d.entries
    print(entries[0].keys())
    # ['title', 'title_detail', 'id', 'guidislink', 'link', 'published', 'published_parsed', 'updated', 'updated_parsed', 'summary', 'summary_detail', 'vrtns_nstag', 'vrtns_nslabeltag', 'links']

    return entries
