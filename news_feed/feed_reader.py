
from typing import Dict, Optional, List, Any
import feedparser


VRT_RSS_URL = 'https://www.vrt.be/vrtnieuws/en.rss.articles.xml'
VRT_RSS_FILE = './tests/resources/en.rss.articles.xml'


def get_rss_feed(source: str) -> Optional[List[Dict[str, Any]]]:
    if source == 'vrt':
        return get_vrt_feed()
    return None


def get_vrt_feed() -> List[Dict[str, Any]]:
    testing = True
    rss_location = VRT_RSS_URL
    if testing:
        rss_location = VRT_RSS_FILE

    d = feedparser.parse(rss_location)
    print(d.keys())
    print(d.feed.keys())
    # ['language', 'title', 'title_detail', 'logo', 'id', 'guidislink', 'link', 'updated', 'updated_parsed', 'authors', 'author_detail', 'author', 'links']
    entries: List[Dict[str, Any]] = d.entries
    print(entries[0].keys())
    # ['title', 'title_detail', 'id', 'guidislink', 'link', 'published', 'published_parsed', 'updated', 'updated_parsed', 'summary', 'summary_detail', 'vrtns_nstag', 'vrtns_nslabeltag', 'links']

    return entries
