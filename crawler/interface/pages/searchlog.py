#!/usr/bin/env python
# -*- coding: utf-8 -*-

from interface.honeycomb import *
import dash_html_components as html
import dash_core_components as dcc
from crawler.utilities.models import *


layout = html.Div([
    html.H3('Search Log',
            style={'text-align': 'center'}),

    html.P('''On this page, you are able to view all searches that are made by users of HIVE. It is not possible
    to clear or delete the search-log.''',
           style={'width': 380,
                  'marginLeft': 'auto',
                  'marginRight': 'auto',
                  'textAlign': 'center',
                  'marginBottom': 10}),


    html.Button('Load table',
                id='reload-button',
                style={'marginLeft': 20,
                       'float': 'right'}),

    html.Br(),

    # html.Div(
    #     dt.DataTable(
    #         sortable=True,
    #         row_selectable=True,
    #         filterable=True,
    #         selected_row_indices=[],
    #         id='keyword-table')
    # ),
], style={'paddingBottom': 55})
