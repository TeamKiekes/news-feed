from __future__ import annotations
from typing import Any, Dict, List, NewType, Type, Union
import feedparser  # type: ignore
from dataclasses import asdict, dataclass
from random import random

VRT_RSS_URL = 'https://www.vrt.be/vrtnieuws/en.rss.articles.xml'
VRT_RSS_FILE = './tests/resources/rss_sources/en.rss.articles.xml'  # Atom
VRT_MAX_ENTRIES = 50
BBC_RSS_URL = 'https://feeds.bbci.co.uk/news/world/rss.xml'
BBC_RSS_FILE = './tests/resources/rss_sources/bbc.world.rss.xml'  # RSS
BBC_MAX_ENTRIES = 23

Feed = List[Dict[str, Any]]
TemporaryFeed = Union[Type[NotImplementedError], Feed]


@dataclass
class FeedConfig:
    name: str
    url: str
    rss_file: str
    max_entries: int


feed_configs = {
    'vrt': FeedConfig('vrt', VRT_RSS_URL, VRT_RSS_FILE, VRT_MAX_ENTRIES),
    'bbc': FeedConfig('vrt', BBC_RSS_URL, BBC_RSS_FILE, BBC_MAX_ENTRIES)
}


@dataclass
class NewsFeed:
    entries: Feed

    @classmethod
    def from_rss_file(cls, config: FeedConfig, skip: int, limit: int, testing: bool = True) -> NewsFeed:

        rss_location = config.url
        if testing:
            rss_location = config.rss_file

        first = skip
        last = skip + limit

        assert first < config.max_entries, f"skip value has to lower than {config.max_entries}."
        assert last < config.max_entries, f"skip + limit value has to lower than {config.max_entries}."
        assert first < last, f"skip value to lower than skip + limit value."
        assert first >= 0, f"skip value has to be positive."
        assert last > 0, f"skip + limit value has greater than 0."

        d = feedparser.parse(rss_location)

        entries: Feed = d.entries[first: last]
        return cls(entries)


@dataclass
class ReducedNewsArticle:
    title: str
    summary: str
    link: str
    published_parsed: List[int]
    news_rating: int

    @classmethod
    def from_feed_article(cls, feed_article: Dict[str, Any]) -> ReducedNewsArticle:
        title = feed_article.get('title', 'no title')
        summary = feed_article.get('summary', 'no summary')
        link = feed_article.get('link', 'no link')
        published_parsed = feed_article.get('published_parsed', 'no published_parsed')
        news_rating = int(random() * 100)
        return cls(title=title, summary=summary, link=link, published_parsed=published_parsed, news_rating=news_rating)


def get_rss_feed(source: str, skip: int, limit: int) -> TemporaryFeed:
    try:
        config = feed_configs[source]
    except KeyError:
        raise NotImplementedError

    feed = NewsFeed.from_rss_file(config, skip, limit)
    reduced_feed: List[ReducedNewsArticle] = [
        ReducedNewsArticle.from_feed_article(article) for article in feed.entries]
    reduced_feed_in_json: Feed = [asdict(article) for article in reduced_feed]
    return reduced_feed_in_json
