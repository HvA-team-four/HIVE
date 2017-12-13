from pony.orm import *
from datetime import datetime
from crawler.utilities.config import *

db = Database()
db.bind(
    provider=configuration_get("database", "provider"),
    user=configuration_get("database", "username"),
    passwd=configuration_get("database", "password"),
    db=configuration_get("database", "database")
)


class Keyword(db.Entity):
    id = PrimaryKey(
        int,
        auto=True
    )
    keyword = Required(
        str, 45
    )
    active = Required(bool)
    content = Set(lambda: Content)


class Url(db.Entity):
    id = PrimaryKey(
        int,
        auto=True
    )
    url = Required(str, 500)
    content = Set(lambda: Content)
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


class Block(db.Entity):
    int = PrimaryKey(
        int,
        auto=True
    )
    type = Required(str)
    value = Required(LongStr)
    active = Required(bool)


# sql_debug(True)
db.generate_mapping(create_tables=True)