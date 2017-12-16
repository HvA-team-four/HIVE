import hashlib
from time import sleep

from bs4 import BeautifulSoup
from pony.orm import *

from utilities.models import *
from utilities import log
from utilities.website import get_content_from_url

@db_session
def get_urls():
    """The get_urls function fetches 16 urls from the database that need to be scraped by the bee.
    The Url which are set with a priority in the database will be retrieved first.
    """
    return select(u for u in Url if u.date_scraped is None).order_by(desc(Url.priority_scrape))[:16]


@db_session
def get_keywords():
    """ The get_keywords function retrieves keywords from the database if they are set to active."""
    return select(k for k in Keyword if k.active)


def filter_keywords(content):
    """The filter_keywords function scans webcontent it receives for matching keywords retrieved from the database.
    Takes (filtered) webcontent as its parameter."""
    # Retrieve keywords from database using the get_keywords function.
    keywords = get_keywords()

    # Create an empty array in which to store matches
    keywords_in_content = []

    # loop through all the keywords and check if they exist in the content. If they do, add them to the array.
    for k in keywords:
        if k.keyword in content:
            keywords_in_content.append(k)

    # return the array with keywords
    return keywords_in_content


@db_session
def save_content(url_id, cleaned, raw, hashed, keywords):
    """The save_content function takes all the contents from the website and stores them into the database.
    The function takes the following arguments:
        **url_id** the id of the url in which matches the contents.
        **cleaned** the plain text of the website.
        **raw** the complete raw contents of the retrieved website
        **hashed** an hashed version of the website. Used for comparisons.
        **keywords** an array with all the matching keywords found on the website.
    """
    try:
        # get url object from database using url_id
        url = select(u for u in Url if u.id == url_id).get()

        # storing raw utf-8 decoded in raw_string
        raw_string = raw.decode('utf-8')

        # set contents to be added to database.
        content_object = Content(
            url=url,
            content=cleaned,
            content_raw=raw_string,
            content_raw_hash=hashed,
            keyword=keywords
        )
        commit()
    except OptimisticCheckError as error:
        print(str(error))

@db_session
def update_url(url):
    """The update_url function sets the date of scraped urls to now."""

    url.date_scraped = datetime.now()


def clean_html(html):
    """The clean_html function cleans the html, css and javascript tags from the raw website content.
    Takes raw content (html) as input"""
    # BeautifulSoup library to clean and use the html5lib parser to parse it
    soup = BeautifulSoup(html, "html5lib")

    # select the tags that must removed
    for s in soup(['script', 'style']):
        s.decompose()

    # remove white spaces
    return ' '.join(soup.stripped_strings)


def hash_content(content):
    """The hash_content function takes the website contents and generate a hash which could be used for comparisons"""
    hash_object = hashlib.sha256(content)
    hex_dig = hash_object.hexdigest()
    return hex_dig


@db_session(optimistic=False)
def start_bee():
    """The start_bee function starts all the tasks related to starting the bee.
    When this function is called the bee will start working."""
    log.debug("Bee has been started")
    while True:
        urls = get_urls()
        # update the url so different instances don't crawl the same url
        for url in urls:
            update_url(url)

        if len(urls) == 0:
            print("No URLs to be crawled, waiting for 60 seconds.")
            log.info('No URLs to be crawled, waiting for 60 seconds.')
            sleep(60)
            commit()
            continue

        for url in urls:
            try:
                content = get_content_from_url(url.url)

                content_hashed = hash_content(content)

                content_cleaned = clean_html(content)

                keywords = filter_keywords(content_cleaned)

                save_content(url.id, content_cleaned, content, content_hashed, keywords)

            except(ValueError, NameError, TypeError) as error:
                log.error(str(error))


if __name__ == '__main__':
    start_bee()
