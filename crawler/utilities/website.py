import socket
import urllib
import urllib.error
import urllib.request

from utilities import log


def get_content_from_url(url):
    """The get_content_from_url function can be used to retrieve(get) the content from an provided URL.
    This function takes one string containing the full url as its parameter.
    """

    #Set the webcontent to None. This is used in the case an url is not working
    webcontent = None

    # try to open the URL  with a timeout of 10 seconds. Excepts catch an exception when it happens and give back an
    # appropriate response.
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

    # Returning the raw webcontent (this includes all kinds of html tags like: <div>)
    return webcontent
