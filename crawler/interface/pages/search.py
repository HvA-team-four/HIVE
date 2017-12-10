#!/usr/bin/env python
# -*- coding: utf-8 -*-

from interface.honeycomb import *
import dash_html_components as html
import dash_core_components as dcc
from crawler.utilities.models import *
import re


@db_session
def normal_search(keywords_array, keywords, start_date, end_date):
    df_id = 0

    dataframe = pd.DataFrame(columns=['id',
                                      'Domain',
                                      'Last Scraped Date',
                                      'Content',
                                      'Link'])

    # Check if start_date is entered, if not set the time to the beginning of time
    if start_date is None:
        dt_start_date = str(datetime.min)
    else:
        dt_start_date = str(datetime.strptime(start_date, '%Y-%m-%d'))

    # check if end_date is entered, if not set the time is set to now
    if end_date is None:
        dt_end_date = str(datetime.now())
    else:
        dt_end_date = str(datetime.strptime(end_date, '%Y-%m-%d'))

    # return empty dataframe if no keywords are entered
    if keywords_array is None:
        return dataframe

    select_query = str(Content.select_by_sql('''SELECT content.id FROM content INNER JOIN url ON content.url = url.id \
    WHERE Match(content) AGAINST ($keywords IN BOOLEAN MODE) AND url.date_scraped <= $dt_end_date AND url.date_scraped >= $dt_start_date'''))

    while True:
            # Execute the query to retrieve contents from database.
            content_objects = eval(select_query)

            for content in content_objects:
                content_keywords = content.content
                for i in keywords_array:
                    content_keywords = re.sub(r'(%s)' % i, r'**\1**', content_keywords, flags=re.I)

                dataframe = dataframe.append({'id': content.id,
                                              'Domain': content.url.url,
                                              'Last Scraped Date': content.url.date_scraped,
                                              'Content': str(content_keywords),
                                              'Link': '/pages/search_results$' + str(df_id)},
                                             ignore_index=True)
                df_id = df_id + 1

            return dataframe


layout = html.Div([
    html.H3('Search',
            style={'text-align': 'center',
                   'marginTop': 50}),

    html.P('Please use input field below to specify a search query.',
           style={'width': 380,
                  'marginLeft': 'auto',
                  'marginRight': 'auto',
                  'textAlign': 'center',
                  'marginBottom': 30}),

    html.Div([
        dcc.Input(
            placeholder='Please enter a search query...',
            id='search_bar',
            required=True
        ),

        html.Br(),

        dcc.DatePickerRange(
            id='normal_date_picker',
            start_date_placeholder_text='Start date',
            end_date_placeholder_text='End date'
        ),

        html.Button('Search',
                    id='normal_search',
                    style={'float': 'right',
                           'marginRight': -20})

    ], style={'width': 700,
              'marginLeft': 'auto',
              'marginRight': 'auto'}),

    html.Div(id='normal_search_results')
])
