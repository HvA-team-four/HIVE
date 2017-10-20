from pony.orm import *
from datetime import datetime

db = Database()
db.bind(
    provider='mysql',
    user='root',
    passwd='root',
    db='scotchbox'
)

class Keyword(db.Entity):
    id = PrimaryKey(
        int,
        auto=True
    )
    keyword = Required(
        str, 45
    )
    content = Set(lambda: Content)

class Url(db.Entity):
    id = PrimaryKey(
        int,
        auto=True
    )
    url = Required(str, 500)
    content = Optional(lambda: Content)
    date_added = Required(datetime)
    date_scraped = Optional(datetime)
    date_scanned = Optional(datetime)
    priority_scrape = Optional(bool)
    priority_scan = Optional(bool)

class Content(db.Entity):
    id = PrimaryKey(
        int,
        auto=True
    )
    keyword = Set(Keyword)
    url = Required(Url)
    content = Required(LongStr)
    content_raw = Required(LongStr)
    content_raw_hash = Required(str)

class Search(db.Entity):
    int = PrimaryKey(
        int,
        auto=True
    )
    query = Required(str)
    date_searched = Required(datetime)

#sql_debug(True) - Debugging currently turned off.
db.generate_mapping(create_tables=True)