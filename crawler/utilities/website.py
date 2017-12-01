import socket
import urllib.request
import urllib.error
import urllib
from utilities import log


# The content_crawler function can be used to crawl content from a specified URL provided as input-parameter.
def get_content_from_url(url):
    # crawls the content
    webcontent = None

    print("Crawling: " + str(url))

    # request to onion site, open url and read contents
    try:
        webcontent = urllib.request.urlopen(url, timeout=10).read()
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print("Error retrieving website: ", url)
        log.error('Data not retrieved from URL: ' + url + ' because error ' + str(error))
    except socket.timeout: 
        print("timeout")
        log.error('Socket timed out, unable to retrieve data from URL: ' + url)
    except ValueError as error:
        print('Incorrect URL: ' + url)
        log.error('An ValueError occurred, maybe url is formatted incorrectly. URL: ' + url + 'error message:'
                  + str(error))
    except Exception as error:
        print("Unexpected error occurred when crawling URL: " + url)
        log.error('Unexpected error occurred when crawling URL: ' + url + 'error message:' + str(error))

    return webcontent
