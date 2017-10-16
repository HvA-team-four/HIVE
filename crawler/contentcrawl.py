import urllib.request
import urllib.error
import urllib
import socks
import socket
from bs4 import BeautifulSoup

url_list=[
  'http://74ypjqjwf6oejmax.onion/',
  'http://idnxcnkne4qt76tg.onion/',
  'http://dppmfxaacucguzpc.onion/',
  'http://3g2upl4pq6kufc4m.onion/'
]

#TOR SETUP GLOBAL Vars
SOCKS_PORT = 9050  # TOR proxy port that is default from torrc, change to whatever torrc is configured to

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",SOCKS_PORT)
socket.socket = socks.socksocket


# Perform DNS resolution through the socket
def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]


socket.getaddrinfo = getaddrinfo


for i in range(len(url_list)): # Loop trough the array of Onion URL's
    webcontent = None
    print("Crawling URL:"+url_list[i])#Print URL die wordt gescraped
    req = urllib.request.Request(url_list[i])# request to onion site

    try:
        response = urllib.request.urlopen(req, timeout=10)
        webcontent = response.read()
        print(webcontent)
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print("Error retrieving website: ", url_list[i])


    """ TODO
    TEMP save in textfile
    betere errorhandling met log file
    """
