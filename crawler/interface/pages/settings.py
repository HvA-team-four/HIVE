from dash.dependencies import  Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import pandas as pd
import plotly

from interface.app import *

from crawler.models import *

with db_session:
    results = select(p for p in Url)[:]

    df = pd.DataFrame(columns=['id', 'url', 'content','date_added','date_scanned','date_scraped',])

    for result in results:
        df = df.append({'id' : result.id,
                        'url': result.url,
                        'content': result.content,
                        'date_added': result.date_added,
                        'date_scanned': result.date_scanned,
                        'date_scraped': result.date_scraped}, ignore_index=True)


layout = html.Div([
    html.H2("Statistics"),
    html.Div(dt.DataTable(rows=df.to_dict('records'),
    row_selectable = True,
    filterable = True,
    sortable = True,
    id = 'datatable-gapminder'
))
])
