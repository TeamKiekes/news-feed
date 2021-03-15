from __future__ import annotations
from typing import Any, Dict, List, Type, Union
import feedparser  # type: ignore
from dataclasses import asdict, dataclass
import random
from pathlib import Path


import news_feed.constants as const

Feed = List[Dict[str, Any]]
TemporaryFeed = Union[Type[NotImplementedError], Feed]


@dataclass
class FeedConfig:
    name: str
    url: str
    rss_file: str
    max_entries: int


feed_configs = {
    'vrt': FeedConfig('vrt', const.VRT_RSS_URL, const.VRT_RSS_FILE, const.VRT_MAX_ENTRIES),
    'bbc': FeedConfig('vrt', const.BBC_RSS_URL, const.BBC_RSS_FILE, const.BBC_MAX_ENTRIES)
}


@dataclass
class NewsFeed:
    entries: Feed

    @classmethod
    def from_rss_config(cls, config: FeedConfig, skip: int, limit: int, testing: bool = True) -> NewsFeed:

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

    @classmethod
    def from_rss_file(cls, file: Path) -> NewsFeed:
        d = feedparser.parse(file)

        entries: Feed = d.entries
        return cls(entries)

    # @staticmethod
    # def get_feed_entries()


@dataclass
class ReducedNewsArticle:
    title: str
    summary: str
    link: str
    published_parsed: List[int]
    image_url: str
    news_rating: int

    @classmethod
    def from_feed_article(cls, feed_article: Dict[str, Any]) -> ReducedNewsArticle:
        title = feed_article.get('title', 'no title')
        summary = feed_article.get('summary', 'no summary')
        link = feed_article.get('link', 'no link')
        published_parsed = feed_article.get('published_parsed', 'no published_parsed')

        image_url = cls._get_image_url(feed_article)

        news_rating = int(random.random() * 100)
        return cls(title=title, summary=summary, link=link,
                   published_parsed=published_parsed, news_rating=news_rating,
                   image_url=image_url)

    @staticmethod
    def _get_image_url(feed_article: Dict[str, Any]) -> str:
        image_url = 'no image url'
        try:
            image_url = feed_article['media_thumbnail'][0]['url']
            # print(f'Got media url {image_url}')
        except KeyError as e:
            # print(f'no media thumbnail for {title}')
            try:
                for link in feed_article['links']:
                    if 'image' in link['type']:
                        image_url = link['href']
                        # print(f'Got link href url {image_url}')
                        break
            except Exception as e:
                print('Something went wrong while getting the image url')
                print(e)
        else:
            pass
        return image_url


def get_rss_feed(source: str, *args: Any, **kwargs: Any) -> TemporaryFeed:
    if source in const.FEED_COUNTRIES:
        return get_rss_feed_v2(source, **kwargs)
    else:
        return get_rss_feed_v1(source, **kwargs)


def get_rss_feed_v1(source: str, skip: int, limit: int, **kwargs: Any) -> TemporaryFeed:

    try:
        config = feed_configs[source]
    except KeyError:
        raise NotImplementedError

    feed = NewsFeed.from_rss_config(config, skip, limit)
    reduced_feed: List[ReducedNewsArticle] = [
        ReducedNewsArticle.from_feed_article(article) for article in feed.entries]
    reduced_feed_in_json: Feed = [asdict(article) for article in reduced_feed]
    return reduced_feed_in_json


def get_rss_feed_v2(source: str, limit: int, **kwargs: Any) -> TemporaryFeed:

    source_dir_name = const.RSS_FILES_DIR / source.lower()
    source_files = source_dir_name.glob('*.xml')
    # print(source_files)

    reduced_feed: List[ReducedNewsArticle] = []
    for file in source_files:
        feed = NewsFeed.from_rss_file(file)
        for article in feed.entries:
            reduced_feed.append(ReducedNewsArticle.from_feed_article(article))

    reduced_feed_in_json: Feed = [asdict(article)
                                  for article in random.choices(reduced_feed, k=limit)]
    return reduced_feed_in_json
