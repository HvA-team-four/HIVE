from interface.index import *
import dash_html_components as html
import dash_core_components as dcc
from crawler.utilities.models import *

layout = html.Div([
    html.H3('Content Block Settings',
            style={'text-align':'center'}),

    html.P('On this page, the content block settings for HIVE can be set. Blocked content will not be stored in the database and will simply be ignored. Please use the controls to define content which needs to be blocked',
           style={'width':380,
                  'marginLeft':'auto',
                  'marginRight':'auto',
                  'textAlign':'center',
                  'marginBottom':10}),







])