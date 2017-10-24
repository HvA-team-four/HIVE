from utilities import log
from utilities.url_util import format_url, get_urls_from_content
from functions import *
from models import *
from datetime import datetime
from time import sleep
from pony.orm import *


@db_session
def save_url(url):
    result = select(p for p in Url if p.url == url).count()
    if result == 0:
        url_object = Url(
            url=url,
            date_added=datetime.now()
        )
        commit()


@db_session
def get_urls():
    return select(u for u in Url if u.date_scanned is None).random(5)


@db_session
def update_url(url):
    url.date_scanned = datetime.now()
    url.priority_scan = False


@db_session
def start_scout():
    while True:
        urls = get_urls()

        if len(urls) == 0:
            print("No URLs to be crawled, waiting for 60 seconds.")
            sleep(60)
            continue

        for url in urls:
            try:
                # url.url = encryption.hive_decrypt(url.url)
                data = content_crawler(url.url)

                filtered_urls = get_urls_from_content(data)
                for filtered_url in filtered_urls:
                    formatted_url = format_url(url.url, filtered_url)
                    save_url(formatted_url)

            except(ValueError, NameError, TypeError) as error:
                log.error(str(error))
            finally:
                update_url(url)


start_scout()
