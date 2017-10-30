from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def get_urls_from_content(content):
    soup = BeautifulSoup(content, "html5lib")
    urls = []

    for link in soup.find_all('a'):
        urls.append(link.get('href'))

    return urls


def format_url(base_url, other_url):
    other_url = other_url.rstrip("//")
    parsed_other_url = urlparse(other_url)
    result = None

    try:
        if parsed_other_url.netloc == "" and parsed_other_url.path[0] == "/":
            result = urljoin(base_url, other_url).geturl()
        elif parsed_other_url.netloc != "":
            result = other_url
    finally:
        return result
