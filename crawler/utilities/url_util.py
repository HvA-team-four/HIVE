from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def get_urls_from_content(content):
    soup = BeautifulSoup(content, "html5lib")
    urls = []

    for link in soup.find_all('a'):
        if link.get('href') is not None:
            urls.append(link.get('href'))

    return urls


def format_url(base_url, other_url):
    joined_url = urljoin(base_url, other_url)
    parsed_url = urlparse(joined_url)
    if parsed_url.scheme == "http" or "https":
        return urljoin(base_url, other_url)
    return None
