from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_urls_from_content(content):
    soup = BeautifulSoup(content, "html5lib")
    urls = []

    for link in soup.find_all('a'):
        urls.append(link.get('href'))

    return urls


def format_url(base_url, other_url):
    parsed_base_url = urlparse(base_url)
    parsed_other_url = urlparse(other_url)

    if parsed_other_url.netloc is None:
        parsed_other_url._replace(netloc=parsed_base_url.netloc)

    return parsed_other_url.geturl()
