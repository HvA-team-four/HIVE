#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
from utilities.models import *
from honeycomb import *


@db_session
def save_query(keywords, start_date, end_date):
    """The save_query function takes the keywords, start_date and end_date and stores the query in the database.
    These queries can be retrieved to view what users have been looking for"""

    # Composing the string
    search_type = 'Keyword Search for "'
    keywords_search = ', '.join(map(str, keywords))
    start_date_search = str(start_date)
    end_date_search = str(end_date)
    query = search_type + keywords_search + '" From: ' + start_date_search + " Till: " + end_date_search

    # Creating a database object to be stored
    content_object = Search(
        query=query,
        date_searched=datetime.now()
    )

    # Committing the objects and closing the session
    commit()


@db_session
def load_keywords():
    """The load_keywords function is used to reload the keywords table. This function is triggered by a callback.
     The function returns a dataframe containing the results"""

    results = select(p for p in Keyword if p.active)[:]  # Retrieving all keywords from db

    # Creating a dataframe
    df = pd.DataFrame(columns=['label',
                               'value'])

    # Looping through the results and making up a dataframe
    for result in results:
        df = df.append({'label': result.keyword,
                        'value': result.keyword},
                       ignore_index=True)

    return df.to_dict('records')  # Returning the keywords as a table


@db_session
def keyword_search(keywords, start_date, end_date):
    """The keyword_search function takes an array of keywords, a start_date and end_date. It returns a dataframe
    containing the results of de keyword search query
    """

    # df_id is used to increment a dataframe number for the details link
    df_id = 0

    # Creating a dataframe
    dataframe = pd.DataFrame(columns=['id',
                                      'Domain',
                                      'Keywords',
                                      'Last Scraped Date',
                                      'Content',
                                      'Link'])

    # Check if start_date is entered, else set the time to the beginning of time
    if start_date is None:
        dt_start_date = datetime.min
    else:
        dt_start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # check if end_date is entered, else set the time is set to now
    if end_date is None:
        dt_end_date = datetime.now()
    else:
        dt_end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # return empty dataframe if no keywords are entered
    if keywords is None:
        return dataframe

    # The static part of the keyword search query. Contains the search dates
    query = """select(c for c in Content
    if c.url.date_scraped <= dt_end_date
    and c.url.date_scraped >= dt_start_date
    and """

    # Generating the dynamic part of the query, this part contains all the keywords entered
    query += ' in c.keyword.keyword and '.join('"{0}"'.format(w) for w in keywords) + ' in c.keyword.keyword )[:]'

    while True:
            # Execute the query to retrieve contents from database.
            content_objects = eval(query)

            # Generating a dataframe for each found object within the query
            for content in content_objects:
                dataframe = dataframe.append({'id': content.id,
                                              'Domain': content.url.url,
                                              'Keywords': content.keyword.keyword,
                                              'Last Scraped Date': content.url.date_scraped,
                                              'Content': content.content,
                                              'Link': '/pages/results$' + str(df_id)},
                                             ignore_index=True)
                df_id = df_id + 1

            return dataframe


# Defining the lay-out of this page.
layout = html.Div([
    html.H3('Keyword Search',
            style={'text-align': 'center',
                   'marginTop': 50}),

    html.P('Please use the dropdown-bar below to select the keywords you want to search the database for.',
           style={'width': 380,
                  'marginLeft': 'auto',
                  'marginRight': 'auto',
                  'textAlign': 'center',
                  'marginBottom': 30}),

    html.Div([
        dcc.Dropdown(
            options=load_keywords(),
            multi=True,
            id='keywordList'),

    html.Br(),

    dcc.DatePickerRange(
        id='keyword_date_picker',
        start_date_placeholder_text='Start date',
        end_date_placeholder_text='End date'
    ),

    html.Button('Search', id='keyword_search'),
        html.Button('Reload keywords',
                    id='refresh-keyword-list',
                    className='refresh_button',
                    style={'paddingLeft': 10,
                           'paddingRight': 10})
    ], style={'width': 700,
              'marginLeft': 'auto',
              'marginRight': 'auto'}),

    html.Div(id='keyword_search_results')
])
