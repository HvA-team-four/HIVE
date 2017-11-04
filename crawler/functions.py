import socket
import socks
import urllib.request
import urllib.error
import urllib
import logging


# Perform DNS resolution through the socket to translate the DNS names to IP addresses
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]


# Setup the Tor proxy, the socket and perform the dns resolution to translates the domain name into a IPV4 address
def connect_to_tor():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    socket.getaddrinfo = getaddrinfo


# The content_crawler function can be used to crawl content from a specified URL provided as input-parameter.
def content_crawler(url):
    #connect_to_tor()
    # crawls the content
    webcontent = None

    print("Crawling: " + str(url))
    logging.info('Trying to open ' + str(url))

    # request to onion site, open url and read contents
    try:
        webcontent = urllib.request.urlopen(url, timeout=10).read()
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print("Error retrieving website: ", url)
        logging.error('Data not retrieved from URL: ' + url + ' because error ' + str(error))
    except socket.timeout:
        print("timeout")
        logging.error('Socket timed out, unable to retrieve data from URL: ' + url)
    except ValueError as error:
        print('Incorrect URL: ' + url)
        logging.error('An ValueError occurred, maybe url is formatted incorrectly. URL: ' + url + 'error message:'
                      + str(error))
    except Exception as error:
        print("Unexpected error occurred when crawling URL: " + url)
        logging.error('Unexpected error occurred when crawling URL: ' + url + 'error message:' + str(error))
    return webcontent

