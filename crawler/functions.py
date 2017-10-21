# HIVE Framework - This file contains all functions, classes and methods that can be used by the application.

# Import packets
import socket
import socks
from bs4 import *
import urllib.request
import urllib.error
import urllib
import logging
import os
import configparser



# The setup_logfile function can be used to setup a log file
def setup_logfile(name):
    # Setting up logging
    if not os.path.exists("logs/"):
        try:
            os.makedirs("logs/")
        except OSError as error:
            logging.error("Error creating logs directory" + str(error))

    logging.basicConfig(filename='logs/' + str(name) + '.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
    logging.info('\n----------------------------------------------------------------------------------------'
                 '\n Logging started')

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
    word = ".onion"
    for url in arrayurl: # Loop through arrayurl
        if isinstance(url, str):
            if len(url) < 256:
                if url.startswith('/'): # Check if URL is a relative URL
                    appendedurl = baseurl + url # Add the URL if the URL is a relative
                    if appendedurl.startswith('https://') or appendedurl.startswith('http://') and word in appendedurl:
                        urlArray.append(appendedurl) # Add the URL to the urlArray
                else:
                    if word in url:
                        urlArray.append(url) # Add the URL to the urlArray

    return urlArray # Return the urlArray

# The content_crawler function can be used to crawl content from a specified URL provided as input-parameter.
def content_crawler(url):
    connect_to_tor()
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

####################################################
# Configuration Functions
####################################################
# Configuration_get function, please provide a section- and key name and the function returns the value.
def configuration_get(section, key):
    Config = configparser.ConfigParser()
    Config.read("configuration/configuration.ini")
    try:
        configuration_value = Config.get(section, key)
        return configuration_value

    except(ValueError, NameError):
        print("Something went wrong with retrieving the value.")


# Configuration_set function, please provide a section-, key- and value-name and the function sets this value in the file.
def configuration_set(section, key, value):
    Config = configparser.ConfigParser()
    Config.read("configuration/configuration.ini")
    ConfigFile = open("configuration/configuration.ini", 'w')
    try:
        Config.set(section, key, value)

    except(configparser.NoSectionError, configparser.NoOptionError):
        print("This option or section does not exist.")

    Config.write(ConfigFile)
    ConfigFile.close()











    # from cryptography.fernet import Fernet
    #
    # key = Fernet.generate_key()
    # hive = Fernet(key)
    #
    #
    # text = "Toine Lambalk how are you"
    # message = text.encode('utf-8')
    #
    # encrypted = hive.encrypt(message)
    #
    # message = hive.decrypt(encrypted)
    #
    # test = message.decode('utf-8')
    # print(test)
    #
    #
    # print(key)
