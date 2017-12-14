#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html

from utilities.models import *
from honeycomb import *


@db_session
def load_statistics(statistic):
    if statistic == 'total':
        return select(p for p in Block if p.active).count()

    elif statistic == 'urltype':
        return select(p for p in Block if p.type == 'Url' and p.active).count()

    elif statistic == 'keywordtype':
        return select(p for p in Block if p.type == 'Keyword' and p.active).count()


df = pd.DataFrame(columns=['Type',
                           'Value',
                           'Status'])

df = df.append({'Type': 'No data loaded'}, ignore_index=True)

layout = html.Div([
    html.H3('Content Block Settings',
            style={'text-align': 'center'}),

    html.P('''On this page, the content block settings for HIVE can be set. 
    Blocked content will not be stored in the database and will simply be ignored. 
    The statistics are refreshed every 30 seconds. Read the User Guide before using this feature.''',
           style={'width': 380,
                  'marginLeft': 'auto',
                  'marginRight': 'auto',
                  'textAlign': 'center',
                  'marginBottom': 10}),

    html.Div([
            html.Div([
                html.Div(children=load_statistics('total'),
                         id='BlockStatisticsBox1',
                         className='statisticsBox'),
                html.Div(children='Total',
                         className='title'),
                html.Div(children='Amount of active rules in the database',
                         className='description')
            ], className='statisticsWrapper'),

            html.Div([
                html.Div(children=load_statistics('urltype'),
                         className='statisticsBox',
                         id='BlockStatisticsBox2'),
                html.Div(children='URL',
                         className='title'),
                html.Div(children='Amount of active URL rules',
                         className='description')
            ], className='statisticsWrapper'),

            html.Div([
                html.Div(children=load_statistics('keywordtype'),
                         className='statisticsBox',
                         id='BlockStatisticsBox3'),
                html.Div(children='Keyword',
                         className='title'),
                html.Div(children='Amount of active Keyword rules',
                         className='description')
            ], className='statisticsWrapper'),

            html.Button('Refresh statistics',
                        id='refresh-block-statistics',
                        className='refresh_button')
        ], className='statisticsRow'),

    html.Div([
            dcc.Input(id='block-input-box',
                      type='text',
                      style={'width': 480},
                      placeholder='String-match which needs to be blocked'),

            dcc.RadioItems(
                id='block-category',
                options=[
                    {'label': 'Keyword',
                     'value': 'Keyword'},
                    {'label': 'URL',
                     'value': 'Url'}
                ],
                value='Keyword',
                labelStyle={'display': 'inline-block'}),

            html.Button('Submit',
                        id='blocksubmit',
                        style={'marginLeft': 20}),

            html.Button('Load table',
                        id='reload-button',
                        style={'marginLeft': 20,
                               'float': 'right'}),

            html.Br(),
            html.Br(),

            html.Div(id='output-container-block')
    ]),

    html.Br(),

    html.Div(
        dt.DataTable(
            rows=df.to_dict('records'),
            sortable=True,
            row_selectable=True,
            filterable=True,
            selected_row_indices=[],
            id='block-table')
        ),

        html.Button('Set active',
                    id='block_set_active',
                    style={'marginTop': 20,
                           'float': 'left'}),

        html.Div(id='block_activate_warning'),

        html.Button('Set inactive',
                    id='block_set_inactive',
                    style={'marginTop': 20,
                           'marginLeft': 20,
                           'float': 'left'}),

        html.Div(id='block_inactivate_warning')
], style={'paddingBottom': 55})
