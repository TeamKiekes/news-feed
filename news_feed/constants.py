from pathlib import Path

VRT_RSS_URL = 'https://www.vrt.be/vrtnieuws/en.rss.articles.xml'
VRT_RSS_FILE = './tests/resources/rss_sources/en.rss.articles.xml'  # Atom
VRT_MAX_ENTRIES = 50
BBC_RSS_URL = 'https://feeds.bbci.co.uk/news/world/rss.xml'
BBC_RSS_FILE = './tests/resources/rss_sources/bbc.world.rss.xml'  # RSS
BBC_MAX_ENTRIES = 23

RESOURCES_DIR = Path('news_feed/resources')
RSS_FILES_DIR = RESOURCES_DIR / 'RSS_files'
FAILED_RSS_FILES_DIR = RESOURCES_DIR / 'failed_RSS_files'

FEED_COUNTRIES = ['belgium', 'uk']
