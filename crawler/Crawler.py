import urllib
#import urllib.request
import socks
import socket
from bs4 import BeautifulSoup

onion = 'http://74ypjqjwf6oejmax.onion/' #union URL

#TOR SETUP GLOBAL Vars
SOCKS_PORT = 9050  # TOR proxy port that is default from torrc, change to whatever torrc is configured to

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket
def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo

#def getContent(onionsite):	
req = urllib.request.Request(onion) #request to onion site
response = urllib.request.urlopen(req) #opens url
webContent = response.read() #read url
#print (webContent)
	
def clean_me(html): #clean the html, css and javascript tags
    soup = BeautifulSoup(html, "html5lib") #BeatuifulSoup library to clean it and use the html5lib parser to parse it
    for s in soup(['script', 'style']): #select the tags that must removed
        s.decompose() #remove the css and javascript tags
    return ' '.join(soup.stripped_strings) #remove blank lines   

cleaned = clean_me(webContent) #cleans the content

print (cleaned) #print the content

