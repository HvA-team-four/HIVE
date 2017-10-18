import urllib.request
import urllib.error
import urllib
import socks
import socket
import logging
from socket import timeout

url_list=[
  'http://74ypjqjwf6oejmax.onion/',
  'http://idnxcnkne4qt76tg.onion/',
  'http://dppmfxaacucguzpc.onion/',
  'http://3g2upl4pq6kufc4m.onion/'
]

#Setting up logging
logging.basicConfig(filename='logging.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
logging.info('\n----------------------------------------------------------------------------------------'
             '\n Logging started')

#TOR SETUP GLOBAL Vars
SOCKS_PORT = 9050  # TOR proxy port that is default from torrc, change to whatever torrc is configured to

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",SOCKS_PORT)
socket.socket = socks.socksocket


# Perform DNS resolution through the socket
def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]


socket.getaddrinfo = getaddrinfo

i = 1
for url in url_list: # Loop trough the array of Onion URL's
    webcontent = None
    print("Crawling URL:"+url)#Print URL die wordt gescraped
    logging.info('Trying to open ' + url)#Plaats in logfile

    # request to onion site, open url and read contents
    try:
        webcontent = urllib.request.urlopen(url, timeout=10).read()
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print("Error retrieving website: ", url)
        logging.error('Data not retrieved from URL: ' + url + ' because error ' + str(error))
    except timeout:
        print("timeout")

    if webcontent is not None:
        logging.info('Contents of website written to: ' + (str(i) + '.txt'))
        text_file = open(str(i) + ".txt", "w")
        text_file.write("%s" % webcontent)
        i += 1

