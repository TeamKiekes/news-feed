import requests
import json
import fire
import feedparser  # type: ignore
from typing import Optional
import news_feed.constants as const


def get_valid_rss_version():
    d = feedparser.api.SUPPORTED_VERSIONS
    del d['']
    return d


VALID_RSS_VERSION = get_valid_rss_version()


def fetch_rss_file(country_code: Optional[str] = None) -> None:
    input_file = const.RESOURCES_DIR / 'news_feed_list_countries.json'

    with input_file.open('r') as f:
        feed_list = json.load(f)

    country_name = feed_list[country_code]['name'].lower()
    country_sources = feed_list[country_code]['sources']
    country_dir = const.RSS_FILES_DIR / country_name
    country_dir.mkdir(parents=True, exist_ok=True)

    failed_sources = {key: value for key,
                      value in feed_list[country_code].items() if key != 'sources'}
    failed_sources['sources'] = []

    for source in country_sources:
        source_name: str = source["name"]
        print(f'Fetching RSS file of {source_name}')
        rss_url = source['feedlink']
        # TODO make async?
        # TODO: Try https first?
        try:
            response = requests.get(rss_url, allow_redirects=True, timeout=2)
        except TimeoutError as e:
            print(f'Skipping {source_name} due to request time out.')
            continue
        except Exception as e:
            print(f'Skipping {source_name} due to request error \n{e}')
            continue

        if not response.ok:
            print(f'Skipping {source_name} due to bad response.')
            continue

        file_name = f'{source_name.replace(" ", "_")}.xml'

        rss_file = response.content
        if not is_valid_rss(rss_file.decode()):
            print(f'Skipping {source_name} due to invalid RSS file.')
            failed_sources['sources'].append(source)
            continue

        with (country_dir / file_name).open('wb') as out:
            out.write(rss_file)

    if failed_sources['sources']:
        failed_country_dir = const.FAILED_RSS_FILES_DIR
        failed_country_dir.mkdir(parents=True, exist_ok=True)
        with (failed_country_dir / f'{country_name}.json').open('w') as out:
            json.dump(failed_sources, out, indent=4)


def is_valid_rss(content: str):
    d = feedparser.parse(content)
    if d.bozo or d.version not in VALID_RSS_VERSION:
        return False

    return True


def cli():
    """
    Fetch country RSS files.
    Call from root with `poetry run fetch -c <country_code>.
    """
    fire.Fire(fetch_rss_file)
