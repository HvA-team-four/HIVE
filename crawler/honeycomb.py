from models import *

@db_session
def retrieve_keywords():
    keywords = select(p for p in Keyword)

    keywords = keywords.to_json()

    return keywords