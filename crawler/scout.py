from time import sleep
import asyncio

from utilities.url_util import get_urls_from_content, format_url
from utilities.models import *
from utilities import log
from utilities import tor


@db_session
def save_url(url):
    result = select(u for u in Url if u.url == url).count()
    if result == 0:
        url_object = Url(
            url=url,
            date_added=datetime.now()
        )
        commit()


@db_session
def update_url(url):
    url_db = select(u for u in Url if u.id == url.id).get()
    url_db.date_scanned = datetime.now()
    url_db.priority_scan = False


@db_session
def get_urls_from_database():
    return select(u for u in Url if u.date_scanned is None).order_by(desc(Url.priority_scan))[:16]


def get_urls_from_results(urls, results):
    urls_in_results = []
    for index, url in enumerate(urls):
        if type(results[index]) is not bytes:
            continue

        urls_in_content = get_urls_from_content(results[index])
        for url_in_content in urls_in_content:
            urls_in_results.append(format_url(url.url, url_in_content))

    return urls_in_results


@db_session
async def main(loop):
    log.debug('scout has been started')
    while True:
        urls = get_urls_from_database()

        if len(urls) == 0:
            print("No URLs to be crawled, waiting for 60 seconds.")
            log.info('No URLs to be crawled, waiting for 60 seconds.')
            sleep(60)
            continue

        results = await tor.get_content_from_urls(loop, urls)
        # Update urls after crawling
        for url in urls:
            update_url(url)

        urls_from_content = get_urls_from_results(urls, results)

        for u in urls_from_content:
            if u is not None:
                save_url(u)
        print('Saved ', len(urls_from_content), ' new urls')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

