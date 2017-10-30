from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import pandas as pd
import plotly

from interface.app import *

from crawler.models import *

with db_session:
    results = select(p for p in Url)[:]

    df = pd.DataFrame(columns=['URL','Date Added','Date Scan','Datum Scrape','Priority Scrape','Priority Scan'])

    for result in results:
        if result.priority_scan == True:
            priorityscan = 'Yes'
        else:
            priorityscan = 'No'
        if result.priority_scrape == True:
            priorityscrape ='Yes'
        else:
            priorityscrape = 'No'

        df = df.append({'URL': result.url,
                        'Date Added': result.date_added,
                        'Date Scan': result.date_scanned,
                        'Datum Scrape': result.date_scraped,
                        'Priority Scrape': priorityscrape,
                        'Priority Scan': priorityscan}, ignore_index=True)


layout = html.Div([
    html.H3('Settings'),
    html.P('On this page, you are able to add URLs to the database which will automatically receive a priority flag', style={'width':450}),
    html.Div([dcc.Input(id='input-box', type="text", style={'width': 600}, placeholder='URL which need to be added to the database.'),
    html.Button('Submit', id='button'),
    html.Br(),html.Br(),
    html.Div(id='output-container-button',
             children="")]),
    html.Br(),
    html.Div(dt.DataTable(rows=df.to_dict('records'),
        sortable = True,
        id = 'url-table')
    ),
])