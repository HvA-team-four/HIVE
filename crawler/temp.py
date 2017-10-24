from models import Url
from pony.orm import *
from datetime import datetime


with db_session:
    url = Url(
        url="https://reddit.com",
        date_added=datetime.now()
    )