import urllib.request
import socks
import socket
from bs4 import BeautifulSoup

url_list=[
  'http://74ypjqjwf6oejmax.onion/',
  'http://idnxcnkne4qt76tg.onion/',
  'http://dppmfxaacucguzpc.onion/',
  'http://3g2upl4pq6kufc4m.onion/'
]



#onion = 'http://74ypjqjwf6oejmax.onion/' #union URL

#TOR SETUP GLOBAL Vars
SOCKS_PORT = 9050  # TOR proxy port that is default from torrc, change to whatever torrc is configured to

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket
def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo


for i in range(len(url_list)): # Loop trough the array of Onion URL's

    req = urllib.request.Request(url_list[i])  # request to onion site
    response = urllib.request.urlopen(req)  # opens url
    webcontent = response.read()  # read url
    print(webcontent)

    """ TODO
    TEMP save in textfile
    Timeout
    """
