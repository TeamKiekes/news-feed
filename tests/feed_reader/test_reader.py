from news_feed import __version__
import news_feed.constants as const
from pathlib import Path
import feedparser  # type: ignore

import pytest


def get_valid_rss_version():
    d = feedparser.api.SUPPORTED_VERSIONS
    del d['']
    return d


VALID_RSS_VERSION = get_valid_rss_version()
ALL_SOURCES = ['belgium', 'uk']


def get_all_xml_files():
    files = []
    for source in ALL_SOURCES:
        files.extend(get_xml_files_of_source(source))
    return files


def get_xml_files_of_source(source: str):
    source_dir_name = const.RSS_FILES_DIR / source.lower()
    print(source_dir_name)
    return source_dir_name.glob('*.xml')


@pytest.mark.parametrize("file", get_all_xml_files())
def test_if_xml_is_valid_rss(file: Path):
    d = feedparser.parse(file)

    if d.bozo:
        print('\n#####')
        print(f'{file.name} is no valid RSS/XML file.')
        print(d.version)
        print(d.bozo)
        exc = d.bozo_exception
        print(exc)
        print(exc.getLineNumber())
        print(exc.getMessage())
        assert False

    elif d.version not in VALID_RSS_VERSION:
        print('\n#####')
        print(f'{file.name} has no valid RSS version')
        assert False

    else:
        print('\n#####')
        print(file.name)
        print(d.version)
        assert True
