from dash.dependencies import  Input, Output
import dash_html_components as html
import dash_core_components as dcc

from interface.app import *

from crawler.models import *

with db_session:
    results = select(p for p in Url).count()

layout = html.Div([
    html.H2("Statistics"),
    html.H3("Scout"),
    html.P("Amount of URLs in database {}".format(results), style={'maxWidth' : 350, 'marginTop' : -10}, id='resultAmount'),

])
