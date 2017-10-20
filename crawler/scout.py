#!/usr/bin/env python
# File name: scout.py
# Description: this file contains the function for the HIVE component: Scout
# Author: FOUR.
# Date created: 10/14/2017
# Date last modified: 10/14/2017
# Python Version: 3.6


####\    ####\   ####\  ###\          ###\  ############\
#### |   #### |  #### | ### \         ###|  ############|
#### |   #### |  #### |  ### \       ### /  #### |
############# |  #### |   ### \     ### /   #### |
############# |  #### |    ### \   ### /    ############|
#### |   #### |  #### |     ### \ ### /     #### |
#### |   #### |  #### |      ### ### /      #### |
#### |   #### |  #### |       ##### /       ############|
####/    ####/   ####/         ###_/        ############/


# Import necessary packets and modules
from functions import *
from models import *
from datetime import datetime
from time import sleep
from pony.orm import *
import encryption

@db_session
def save_url(url):
    result = select(p for p in Url if p.url == url).count()
    if (result == 0):
        url_object = Url(
            url=url,
            date_added=datetime.now()
        )
        print("Add:", str(url))
        commit()
    else:
        print("Skipped:", str(url))

@db_session
def start_scout():
    # url_object = Url(
    #     url=encryption.hive_encrypt("https://www.msn.com"),
    #     date_added=datetime.now()
    # )
    # commit()

    setup_logfile("scout")

    while True:
        urls = select(p for p in Url if p.date_scanned == None).random(5)

        if len(urls) == 0:
            print("No URLs to be crawled, waiting for 60 seconds.")
            sleep(60)
            continue

        for url in urls:
            try:
                url.url = encryption.hive_decrypt(url.url)
                data = content_crawler(url.url)

                filtered_urls = filterurls(data)

                formatted_urls = urlformat(url.url, filtered_urls) # Turn the content in a list of URLs

                for formatted_url in formatted_urls:
                    print("Adding", str(formatted_url))
                    save_url(encryption.hive_encrypt(formatted_url))

                url.date_scanned = datetime.now()
                url.url = encryption.hive_encrypt(url.url)
                commit()
                break

            except(ValueError, NameError, TypeError) as error:
                logging.error('An error occurred in scout.py' + str(error))
                url.date_scanned = datetime.now()
                url.url = encryption.hive_encrypt(url.url)
                pass