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
import contentcrawl


@db_session
def save_url(url):
    result = select(p for p in Url if p.url == url).count()
    if (result == 0):
        url_object = Url(
            url=url,
            date_added=datetime.now()
        )
        commit()

@db_session
def get_url_list():
    return select(p for p in Url if p.date_scanned == None).limit(5)


@db_session
def start_scout():
    while True:
        urls = get_url_list()
        print(urls.show())
        print(len(urls))
        if len(urls) == 0:
            sleep(60)
            print("Waiting ")
            continue

        for url in urls:
            data = contentcrawl.content_crawler(url)
            formatted_urls = urlformat(url.url, filterurls(data))  #filterurls(data)) # Turn the content in a list of URLs
            for formatted_url in formatted_urls:
                save_url(formatted_url)

            url.date_scanned = datetime.now()
            commit()


start_scout()

            # if __name__ == "__main__":
            #     start_scout()