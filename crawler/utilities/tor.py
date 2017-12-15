import socket
import socks
from utilities import log
import aiohttp
import async_timeout
import asyncio
from aiosocks.connector import ProxyConnector, ProxyClientRequest


def getaddrinfo(*args):
    """Perform DNS resolution through the socket to translate the DNS names to IP addresses"""
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]


def connect_to_tor():
    """Setup the Tor proxy, the socket and perform the dns resolution to translates the domain name
    into a IPV4 address"""
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    socket.getaddrinfo = getaddrinfo
    log.debug('Setting up socket and connecting to TOR')


async def fetch(session, url):
    """"""
    proxy = 'socks5://127.0.0.1:9050'
    with async_timeout.timeout(10):
        async with session.get(url, proxy=proxy) as response:
            return await response.read()


async def get_content_from_urls(loop, urls):
    conn = ProxyConnector(remote_resolve=True)
    with aiohttp.ClientSession(loop=loop, connector=conn, request_class=ProxyClientRequest) as session:
        return await asyncio.gather(
            *[fetch(session, url.url) for url in urls],
            return_exceptions=True  # default is false, that would raise
        )

