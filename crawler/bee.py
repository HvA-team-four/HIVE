from utilities import log
from functions import *
from models import *
from time import sleep
from pony.orm import *
from bs4 import BeautifulSoup
import hashlib


@db_session
def get_urls():
    return select(u for u in Url if u.date_scraped is None).order_by(desc(Url.priority_scrape))


@db_session
def get_keywords():
    return select(k for k in Keyword if k.active)


def filter_keywords(content):
    keywords = get_keywords()
    keywords_in_content = []
    for k in keywords:
        if k.keyword in content:
            keywords_in_content.append(k)

    return keywords_in_content

@db_session
def save_content(url_id, cleaned, raw, hashed, keywords):
    url = select(u for u in Url if u.id == url_id).get()
    raw_string = raw.decode('utf-8')
    content_object = Content(
        url=url,
        content=cleaned,
        content_raw=raw_string,
        content_raw_hash=hashed,
        keyword=keywords
    )
    commit()


@db_session
def update_url(url):
    url.date_scraped = datetime.now()
    url.priority_scrape = False


def clean_html(html):  # clean the html, css and javascript tags
    soup = BeautifulSoup(html, "html5lib")  # BeatuifulSoup library to clean and use the html5lib parser to parse it
    for s in soup(['script', 'style']):  # select the tags that must removed
        s.decompose()
    return ' '.join(soup.stripped_strings)  # remove white spaces


def hash_content(content):
    hash_object = hashlib.sha256(content)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def start_bee():
    log.debug("Bee has been started")
    while True:
        urls = get_urls()
        if len(urls) == 0:
            print("No URLs to be crawled, waiting for 60 seconds.")
            sleep(60)
            continue

        for url in urls:
            try:
                content = content_crawler(url.url)

                content_hashed = hash_content(content)

                content_cleaned = clean_html(content)

                keywords = filter_keywords(content_cleaned)

                save_content(url.id, content_cleaned, content, content_hashed, keywords)

            except(ValueError, NameError, TypeError) as error:
                log.error(str(error))
            finally:
                update_url(url)

if __name__ == '__main__':
    start_bee()