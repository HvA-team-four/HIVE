#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import dash_core_components as dcc
import dash_html_components as html
from utilities.models import *
from honeycomb import *


# This function is used to save the user's query in the database
# These search queries can be retrieved to view what users have been looking for
@db_session
def save_query(keywords, start_date, end_date):
    """The save_query function takes the keywords, start_date and end_date and stores the query in the database.
    These queries can be retrieved to view what users have been looking for"""
    # Composing the string
    search_type = 'Normal Search for "'
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
def normal_search(keywords_array, keywords, start_date, end_date):
    """The normal_search function takes an array of keywords by user input, a start_date and end_date. It returns a dataframe
    containing the results of de search query
    """

    # df_id is used to increment a dataframe number for the details link
    df_id = 0

    # Creating a dataframe
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

    #select the id of the specific content that contains the keywords. Also the user can filter on date.
    select_query = str(Content.select_by_sql('''SELECT content.id FROM content INNER JOIN url ON content.url = url.id \
    WHERE Match(content) AGAINST ($keywords IN BOOLEAN MODE) AND url.date_scraped <= $dt_end_date AND url.date_scraped >= $dt_start_date'''))

    while True:
            # Execute the query to retrieve contents from database.
            content_objects = eval(select_query)

            for content in content_objects:
                content_keywords = content.content
                for i in keywords_array:
                    #replace the keyword in the text with stars. The keywords will be displaying as bolt words.
                    content_keywords = re.sub(r'(%s)' % i, r'**\1**', content_keywords, flags=re.I)

                # Generating a dataframe for each found object within the query
                dataframe = dataframe.append({'id': content.id,
                                              'Domain': content.url.url,
                                              'Last Scraped Date': content.url.date_scraped,
                                              'Content': str(content_keywords),
                                              'Link': '/pages/search_results$' + str(df_id)},
                                             ignore_index=True)
                df_id = df_id + 1

            return dataframe


# Defining the lay-out of this page.
layout = html.Div([
    html.Div([
    html.H3('Search',
            style={'text-align': 'center',
                   'marginTop': 50},
            className="page_title_info"),

    html.A('help',
           href="/pages/userguide",
           style={'text-align': 'center',
                  'marginTop': 50,
                  'display': 'inlineBlock'},
           className="page_title_info_bullet"
           ),

    ], className="page_title"),

    html.P('''Please use input field below to specify a search query. Please read the User Guide before using the 
    search functionality.''',
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
