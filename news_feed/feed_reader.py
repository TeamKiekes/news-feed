
from typing import Any, Dict, List, NewType, Type, Union
import feedparser  # type: ignore


VRT_RSS_URL = 'https://www.vrt.be/vrtnieuws/en.rss.articles.xml'
VRT_RSS_FILE = './tests/resources/rss_sources/en.rss.articles.xml'  # Atom
VRT_MAX_ENTRIES = 50
BBC_RSS_URL = 'https://feeds.bbci.co.uk/news/world/rss.xml'
BBC_RSS_FILE = './tests/resources/rss_sources/bbc.world.rss.xml'  # RSS
BBC_MAX_ENTRIES = 23

Feed = NewType('Feed', List[Dict[str, Any]])
TemporaryFeed = Union[Type[NotImplementedError], Feed]


def get_rss_feed(source: str, skip: int, limit: int) -> TemporaryFeed:
    if source == 'vrt':
        return get_vrt_feed(skip, limit)
    if source == 'bbc':
        return get_bbc_feed(skip, limit)
    raise NotImplementedError


def get_vrt_feed(skip: int, limit: int) -> Feed:
    testing = True
    rss_location = VRT_RSS_URL
    if testing:
        rss_location = VRT_RSS_FILE

    first = skip
    last = skip + limit

    assert first < VRT_MAX_ENTRIES, f"skip value has to lower than {VRT_MAX_ENTRIES}."
    assert last < VRT_MAX_ENTRIES, f"skip + limit value has to lower than {VRT_MAX_ENTRIES}."
    assert first < last, f"skip value to lower than skip + limit value."
    assert first >= 0, f"skip value has to be positive."
    assert last > 0, f"skip + limit value has greater than 0."

    d = feedparser.parse(rss_location)
    # print(d.keys())
    # print(d.feed.keys())
    # ['language', 'title', 'title_detail', 'logo', 'id', 'guidislink', 'link', 'updated', 'updated_parsed', 'authors', 'author_detail', 'author', 'links']
    entries: Feed = d.entries[first: last]
    # print(entries[0].keys())
    # ['title', 'title_detail', 'id', 'guidislink', 'link', 'published', 'published_parsed', 'updated', 'updated_parsed', 'summary', 'summary_detail', 'vrtns_nstag', 'vrtns_nslabeltag', 'links']

    return entries


def get_bbc_feed(skip: int, limit: int) -> Feed:
    testing = True
    rss_location = BBC_RSS_URL
    if testing:
        rss_location = BBC_RSS_FILE

    first = skip
    last = skip + limit

    assert first < BBC_MAX_ENTRIES, f"skip value has to lower than {BBC_MAX_ENTRIES}."
    assert last < BBC_MAX_ENTRIES, f"skip + limit value has to lower than {BBC_MAX_ENTRIES}."
    assert first < last, f"skip value to lower than skip + limit value."
    assert first >= 0, f"skip value has to be positive."
    assert last > 0, f"skip + limit value has greater than 0."

    d = feedparser.parse(rss_location)
    # print(d.keys())
    # print(d.feed.keys())
    # ['language', 'title', 'title_detail', 'logo', 'id', 'guidislink', 'link', 'updated', 'updated_parsed', 'authors', 'author_detail', 'author', 'links']
    entries: Feed = d.entries[first: last]
    # print(entries[0].keys())
    # ['title', 'title_detail', 'id', 'guidislink', 'link', 'published', 'published_parsed', 'updated', 'updated_parsed', 'summary', 'summary_detail', 'vrtns_nstag', 'vrtns_nslabeltag', 'links']

    return entries
