from utilities import log
from utilities.url_util import format_url, get_urls_from_content
from functions import *
from models import *
from datetime import datetime
from time import sleep
from pony.orm import *
from bs4 import BeautifulSoup
from interface.index import *
import dash_html_components as html
import dash_core_components as dcc

# FILE FOR DEVELOPMENT PURPOSES ONLY!!!

keywords2 = ("Hacker", "da", "hack3")



@db_session
def keyword_search(keywords):
    df = pd.DataFrame(columns=['url',
                               'Keywords',
                               'content'
                               'content_raw'])

    for keyword in keywords:
        content_objects = select(c for c in Content if keyword in c.keyword.keyword)[:]

        for content in content_objects:
            kw = []
            for keyword2 in content.keyword.keyword:
                kw.append(keyword2)
            df = df.append({'url': content.url.url,
                            'keywords': kw,
                            'content': content.content,
                            'content_raw': content.content_raw},
                           ignore_index=True)

        return df.to_dict('Results')





#Get keywords from database
@db_session
def get_keywords():
    keywords = select(p for p in Keyword)
    return keywords


def filter_keywords(webcontent):
    keywords = get_keywords()
    found = []
    for keyword in keywords:
        word = keyword.keyword
        if word in webcontent:
            log.debug('keyword found: ' + word)
            found.append(keyword)
    return found

@db_session
def store_keywords(keyword, url_id):
    url = select(u for u in Url if u.url == url_id).get()
    content = select(c for c in Content if c.url == url)
    contentkeyword_object = content_keyword(
        content=content,
        keyword=keyword
    )
    commit()

@db_session
def start_keyword():
    result = keyword_search(keywords2)
    log.debug(str(result))



start_keyword()