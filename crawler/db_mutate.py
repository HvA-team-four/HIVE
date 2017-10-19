from models import *
from datetime import *
from pony.orm import *

@db_session
def add_url_manually(url):
    url_object = Url(
        url=url,
        date_added=datetime.now()
    )
    print("URL Added to database" + str(url))
    commit()

@db_session
def delete_url_manually(url):
    delete(p for p in Url if p.url == url)
    print("URL Deleted" + str(url))
    commit()

@db_session
def check_table_manually(table):
    results = select(p for p in table)[:]
    for url in results:
        print(url.url)

@db_session
def emtpy_table_manually(table):
        delete(p for p in table)

check_table_manually(Url)

