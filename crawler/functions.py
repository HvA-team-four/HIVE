# HIVE Framework - This file contains all functions, classes and methods that can be used by the application.

# Import packets
import socks
import socket
from bs4 import *

# Perform DNS resolution through the socket to translate the DNS names to IP addresses
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

# Setup the Tor proxy, the socket and perform the dns resolution to translates the domain name into a IPV4 address
def connect_to_tor():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    socket.getaddrinfo = getaddrinfo

# The filterurls function can be used to filter URLs from a string input.
def filterurls(content):
    soup = BeautifulSoup(content, "html5lib") # Clean the content
    urlArray = []   # Creating an empty array

    for link in soup.find_all('a'):    # For loop which finds all URLs from the input parameter
        urlArray.append(link.get('href'))   # Add the URLs to an array

    return urlArray # Returns the urlArray variable

# The urlformat function can be used to format URLs for uniform storage. Output is an array.
def urlformat(baseurl, arrayurl):
    baseurl = baseurl.rstrip('//') # Strip the slash from the URL of the baseurl
    urlArray = [] # Creating an empty array

    for url in arrayurl: # Loop through arrayurl
        
        if url.startswith('/'): # Check if URL is a relative URL
            appendedurl = baseurl + url # Add the URL if the URL is a relative
            urlArray.append(appendedurl) # Add the URL to the urlArray
        else:
            urlArray.append(url) # Add the URL to the urlArray

    return urlArray # Return the urlArray