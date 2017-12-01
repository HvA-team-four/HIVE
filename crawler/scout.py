from time import sleep
from utilities.models import *
from utilities import log
from utilities.tor import connect_to_tor
from utilities.url_util import format_url, get_urls_from_content
from utilities.website import get_content_from_url

# Add found URLs to the database if they are not being blocked by the content-block feature.
@db_session
def save_url(url):
    blockedUrls = select(b.value for b in Block if b.type == "Url")[:]

    if not any(x for x in blockedUrls if x in url):
        result = select(p for p in Url if p.url == url).count()
        if result == 0:
            url_object = Url(
                url=url,
                date_added=datetime.now()
            )
    else:
        log.info("URL: {} is blocked".format(url))

    commit()

# Update the URL which was being scraped
@db_session
def update_url(url):
    url.date_scanned = datetime.now()

@db_session
def start_scout():
    log.debug('Scout has been started')

    while True:
        urls = select(u for u in Url if u.date_scanned is None).order_by(desc(Url.priority_scan))[:32]

        if len(urls) == 0:
            print("No URLs to be crawled, waiting for 60 seconds.")
            log.info('No URLs to be crawled, waiting for 60 seconds.')
            sleep(10)
            commit()
            continue

        for url in urls:
            try:
                content = get_content_from_url(url.url)
                content_urls = get_urls_from_content(content)

                for content_url in content_urls:
                    formatted_url = format_url(url.url, content_url)

                    if formatted_url is not None:
                        save_url(formatted_url)

            except(ValueError, NameError, TypeError) as error:
                log.error(str(error))

            finally:
                update_url(url)




if __name__ == '__main__':
    start_scout()
