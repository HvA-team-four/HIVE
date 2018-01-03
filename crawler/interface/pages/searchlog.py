#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_html_components as html
from honeycomb import *

# Creating a dataframe and filling it with one row: No data loaded.
df = pd.DataFrame(columns=['Query',
                           'Date Searched'])

df = df.append({'Query': 'No data loaded'}, ignore_index=True)

# Defining the lay-out of this page.
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

    html.Br(),

html.Br(),

    html.Div(
         dt.DataTable(
            rows=df.to_dict('records'),
            sortable=False,
            filterable=True,
            id='searchlog-table')
    ),
], style={'paddingBottom': 55})
