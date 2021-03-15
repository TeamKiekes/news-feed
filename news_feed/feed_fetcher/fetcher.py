import requests
import json
from typing import Optional

import news_feed.constants as const


def fetch_rss_file(country_code: Optional[str] = None) -> None:
    input_file = const.RESOURCES_DIR / 'news_feed_list_countries.json'

    with input_file.open('r') as f:
        feed_list = json.load(f)

    country_name = feed_list[country_code]['name']
    country_sources = feed_list[country_code]['sources']
    country_dir = const.RSS_FILES_DIR / country_name
    country_dir.mkdir(parents=True, exist_ok=True)

    for source in country_sources:
        source_name: str = source["name"]
        print(f'Fetching RSS file of {source_name}')
        rss_url = source['feedlink']
        # TODO make async
        # TODO remove 404, 403, ...
        # TODO: Try https first
        try:
            response = requests.get(rss_url, allow_redirects=True, timeout=2)
        except TimeoutError as e:
            print(f'Skipping {source_name} due to time out.')
            continue
        except Exception as e:
            print(f'Skipping {source_name} due to error \n{e}')
            continue
        file_name = f'{source_name.replace(" ", "_")}.xml'
        with (country_dir / file_name).open('wb') as out:
            out.write(response.content)


def main() -> None:
    test_country = 'GB'
    fetch_rss_file(test_country)


if __name__ == "__main__":
    main()
