import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
from dash.dependencies import Input, Output, State

from crawler.models import *
from crawler.utilities import config


with db_session:
    query = select(
        (p.id, p.keyword, c.id, c.content, c.keyword, c.url)
        for p in Keyword for c in Content
        if p.keyword == "Hart van Nederland"
    )
    query.show()