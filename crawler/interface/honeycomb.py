#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
from dash.dependencies import Input, Event, Output, State
from interface.elements import header
from interface.elements import eula
from interface.pages import keywordsearch
from interface.pages import keywordsettings
from interface.pages import search
from interface.pages import settings
from interface.pages import start
from interface.pages import urlsettings
from interface.pages import blocksettings
from interface.pages import configurationsettings
from interface.pages import userguide
from crawler.utilities.models import *
from crawler.utilities.config import *
from datetime import datetime
import re

# Defining a Dash application/interface with the name 'app'
app = dash.Dash()

# Defining some parameters of the interface
# Title: the name of the interface (name of tab)
# CSS: Default CSS style sheet provided by Dash
# CSS: Custom CSS style sheet defined in the configuration.ini
app.title = configuration_get("honeycomb", "title")
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.css.append_css({'external_url': configuration_get("styling", "css")})

# Suppressing callback exceptions, otherwise Dash is raising error
# when callbacks are not working correctly
app.config.supress_callback_exceptions = True

# Layout of the application, the layout consist of multiple components
# this lay-out contains the following elements
# Header: default header from the 'header.py'
# Location: used for setting the pathname variable which is used later
# Page-content: this content changed when the user selects another page
# Datatable: hidden, but needed for displaying tables correctly
# Termsboxarea: used for displaying the terms of use when a user selects the EULA
# Interval elements: used for pages which automatically reload
# Termsbox: orange bar defining the EULA which the user agrees to
app.layout = html.Div([
    header.hive_header,

    dcc.Location(id='url',
                 refresh=False),

    html.Div(id='page-content'),

    html.Div(
        dt.DataTable(rows=[{}]),
        style={'display': 'none'}),

    html.Div(children=[], id="TermsBoxArea"),
    dcc.Interval(
            id='interval-component-30',
            interval=20*1000
    ),
    dcc.Interval(
            id='interval-component-5',
            interval=5*1000
    ),
    eula.hive_bottombar
], style={'background': "url('{}')".format(configuration_get("styling", "imagepath") + "branding/background.png"),
          'height': '100%',
          'minHeight': '100vh'})


###################################################################################
# SEARCH pages callback
#
# This block contains all functions which are required for a right
# functioning of the two search pages (normal search, keyword search).
###################################################################################

# Normal search query
@app.callback(Output('normal_search_results', 'children'),
              [Input('normal_search', 'n_clicks')],
              [State('search_bar', 'value'),
               State('normal_date_picker', 'start_date'),
               State('normal_date_picker', 'end_date')])
def display_results(n_clicks, values, start_date, end_date):
    values_array = (re.findall(r"[\w']+", values))

    global df
    df = search.normal_search(values_array, values, start_date, end_date)

    if df.empty:
        results = html.Div([
            html.Div([
                html.H4("Results"),
                html.P(
                    "No results were found based on your search",
                    style={"width": 370,
                           "marginBottom": 15}),
            ], className="content")
        ], className="results_section")
    else:
        results = html.Div([
            html.Div([
                html.H4("Results"),

                html.P('''The following table displays all the search results which were retrieved based 
                on your search query.''',
                       style={"width": 370,
                              "marginBottom": 15}),

                html.Table(
                    [html.Tr([html.Th(col) for col in df.columns], className="tableHeader")] +

                    [html.Tr([
                        html.Td(df.iloc[i]['id'], className="tableData"),
                        html.Td(df.iloc[i]['Domain'], className="tableData"),
                        html.Td(df.iloc[i]['Last Scraped Date'], className="tableData"),
                        html.Td(dcc.Markdown(str(df.iloc[i]['Content'][:75] + (df.iloc[i]['Content'][75:] and '...'))),
                                className="tableData"),
                        html.Td([html.A("Details", href=df.iloc[i]['Link'])], className="tableData")
                    ]) for i in range(len(df))]
                )], className="content")
        ], className="results_section")

    return results


# Callback for refreshing the list of selectable keywords
# this can be done manually but is also refreshed
# automatically every 30 seconds.
@app.callback(Output('keywordList', 'options'),
              [Input('refresh-keyword-list', 'n_clicks')],
              events=[Event('interval-component-30', 'interval')])
def refresh_keyword_list(n_clicks):
    return keywordsearch.load_keywords()


# Keyword search query
@app.callback(Output('keyword_search_results', 'children'),
              [Input('keyword_search', 'n_clicks')],
              [State('keywordList', 'value'),
               State('keyword_date_picker', 'start_date'),
               State('keyword_date_picker', 'end_date')])
def display_results(n_clicks, values, start_date, end_date):
    keywordsearch.save_query(values, start_date, end_date) # Save query in database

    global df
    df = keywordsearch.keyword_search(values, start_date, end_date) # Search query

    if df.empty:
        results = html.Div([
            html.Div([
                html.H4("Results"),
                html.P(
                    "No results were found based on your keyword search",
                    style={"width": 370,
                           "marginBottom": 15}),
                ], className="content")
            ], className="results_section")
    else:
        results = html.Div([
            html.Div([
                html.H4("Results"),
                html.P('''The following table displays all the search results which were retrieved based 
                on your search query.''',
                       style={"width": 370,
                              "marginBottom": 15}),

                html.Table(
                    [html.Tr([html.Th(col) for col in df.columns], className="tableHeader")] +

                    [html.Tr([
                        html.Td(df.iloc[i]['id'], className="tableData"),
                        html.Td(df.iloc[i]['Domain'], className="tableData"),
                        html.Td(", ".join(df.iloc[i]['Keywords']), className="tableData"),
                        html.Td(df.iloc[i]['Last Scraped Date'], className="tableData"),
                        html.Td(df.iloc[i]['Content'][:75] + (df.iloc[i]['Content'][75:] and '...'), className="tableData"),
                        html.Td([html.A("Details", href=df.iloc[i]['Link'])], className="tableData")
                    ]) for i in range(len(df))]
                )], className="content")
        ], className="results_section")

    return results


###################################################################################
# SETTINGS pages callback
#
# This block contains all functions which are required for the application's
# settings page functions and the User Guide page.
###################################################################################


####################
# Keyword settings
####################


# Loading the value of StatisticsBox one - total amount of KEYWORDS
@app.callback(Output('KeywordStatisticsBox1', 'children'),
              [Input('refresh-keyword-statistics', 'n_clicks')],
              events=[Event('interval-component-30', 'interval')])
def refresh_keyword_statistics(n_clicks):
    return keywordsettings.load_statistics('total')  # Parameter total indicates the total amount of keywords


# Loading the value of StatisticsBox two - total amount of active KEYWORDS
@app.callback(Output('KeywordStatisticsBox2', 'children'),
              [Input('refresh-keyword-statistics', 'n_clicks')],
              events=[Event('interval-component-30', 'interval')])
def refresh_keyword_statistics(n_clicks):
    return keywordsettings.load_statistics('active')  # Parameter active indicates the active amount of keywords


# Loading the value of StatisticsBox three - no information yet
@app.callback(Output('KeywordStatisticsBox3', 'children'),
              [Input('refresh-keyword-statistics', 'n_clicks')],
              events=[Event('interval-component-30', 'interval')])
def refresh_keyword_statistics(n_clicks):
    return keywordsettings.load_statistics('matches')  # Parameter matches shows the amount of keyword matches


# Callback for adding KEYWORDS to the database
@app.callback(Output('output-container-keyword', 'children'),
              [Input('keywordsubmit', 'n_clicks')],
              [State('keyword-input-box', 'value')])
@db_session
def insert_keyword(n_clicks, value):
    result = select(p for p in Keyword if p.keyword == value).count()  # Retrieving the amount of keywords

    if not value:  # If the user has not submitted anything in the input field
        return html.Div('Please insert a value in the input field.',  # Output warning message
                        id='negative_warning') # Negative style (red)

    elif result != 0:  # Check if the keyword already exists in the database
        return html.Div('Keyword already exists in database',  # Output warning message
                        id='negative_warning') # Negative style (red)

    else:  # If keyword does not exist yet
        try:  # Trying
            keyword_object = Keyword(
                keyword=value,
                active=True
            )  # Defining an object of class Keyword
            commit()  # Committing the object (sending it to database)

            return html.Div('Keyword: {} has been added to the database.'.format(value),  # Output warning message
                            id='positive_warning')  # Positive style (green)

        except:
            return html.Div('An unexpected error occurred',  # Output warning message
                            id='negative_warning')  # Negative style (red)


# Callback used for loading the KEYWORD table on the KEYWORD Settings page
@app.callback(Output('keyword-table', 'rows'),
              [Input('reload-button', 'n_clicks')])
@db_session
def reload_table(n_clicks):
    results = select(p for p in Keyword)[:]  # Retrieving all keywords from the database

    global df  # Defining a global dataframe so the keywords can be loaded from the keywords search page

    df = pd.DataFrame(columns=['Keyword',  # Defining a dataframe with the columns: keyword and status
                               'Status'])

    for result in results:  # For each keyword in the table do:
        if result.active:  # If the active column is true, then set status equal to the word Active
            status = 'Active'

        else:  # If not active then say Inactive
            status = 'Inactive'

        df = df.append({'Keyword': result.keyword,
                        'Status': status},
                       ignore_index=True)  # Add the record to a dataframe which can then be displayed in the table

    return df.to_dict('records')  # Return each record in the dataframe as a dictionary.


# Callback for turning KEYWORDS ACTIVE
@app.callback(Output('activate_warning', 'children'),
              [Input('keyword_set_active', 'n_clicks')],
              [State('keyword-table', 'selected_row_indices')])
@db_session
def insert_url(n_clicks, selected_row_indices):
    try:  # Try changing, if anything goes wrong, a warning message will be displayed instead of an application crash
        if 'df' not in globals():  # Check if the table is loaded
            return html.Div('Please load the keyword table first.',  # Warning message
                            id='negative_warning')  # Red style (error style)

        elif not selected_row_indices:  # If there are no rows selected
            return html.Div('Please select a keyword.',  # Warning message
                            id='negative_warning')  # Red style (error style)

        else:
            records = df.iloc[selected_row_indices].Keyword  # Retrieve the selected rows from the dataframe variable

            for record in records:  # For each selected keyword
                results = select(p for p in Keyword if p.keyword == record)  # Retrieve the keyword object

                for result in results:  # This needs to be unwrapped because the result is a ponyORM object.
                    result.active = True  # Setting the active field to true
                    commit()  # Committing the action

            return html.Div('The selected records are set active.',  # Warning message
                            id='positive_warning')  # Green style (positive style)

    except:  # If anything unexpected occurs
        return html.Div('An unexpected error occurred.',  # Warning messsage
                        id='negative_warning')  # Red style (error style)


# Callback for turning KEYWORDS INACTIVE
@app.callback(Output('inactivate_warning', 'children'),
              [Input('keyword_set_inactive', 'n_clicks')],
              [State('keyword-table', 'selected_row_indices')])
@db_session
def insert_url(n_clicks, selected_row_indices):
    try:  # Try changing, if anything goes wrong, a warning message will be displayed instead of an application crash
        if 'df' not in globals():  # Check if the table is loaded
            return html.Div('Please load the keyword table first.',  # Warning message
                            id='negative_warning')  # Red style (error style)

        elif not selected_row_indices:  # If there are no rows selected
            return html.Div('Please select a keyword.',  # Warning message
                            id='negative_warning')  # Red style (error style)

        else:
            records = df.iloc[selected_row_indices].Keyword  # Retrieve the selected rows from the dataframe variable

            for record in records:  # For each selected keyword
                results = select(p for p in Keyword if p.keyword == record)  # Retrieve the keyword object

                for result in results:  # This needs to be unwrapped because the result is a ponyORM object.
                    result.active = False  # Setting the active field to false
                    commit()  # Comitting the action

            return html.Div('The selected records are set inactive.',  # Warning message
                            id='positive_warning')  # Green style (positive style)

    except:  # If anything unexpected occurs
        return html.Div('An unexpected error occurred.',  # Warning messsage
                        id='negative_warning')  # Red style (error style)


################
# URL settings
################


# Loading the value of StatisticsBox one - total amount of URLs in the database
@app.callback(Output('UrlStatisticsBox1', 'children'),
              [Input('refresh-url-statistics', 'n_clicks')],
              events=[Event('interval-component-5', 'interval')])
def refresh_url_statistics(n_clicks):
    return urlsettings.load_statistics('total')  # Parameter total indicates the total amount of keywords


# Loading the value of StatisticsBox two - total amount of scanned URLs
@app.callback(Output('UrlStatisticsBox2', 'children'),
              [Input('refresh-url-statistics', 'n_clicks')],
              events=[Event('interval-component-5', 'interval')])
def refresh_url_statistics(n_clicks):
    return urlsettings.load_statistics('scanned')  # Parameter scanned indicates the scanned amount of keywords


# Loading the value of StatisticsBox three - total amount of scraped URLs
@app.callback(Output('UrlStatisticsBox3', 'children'),
              [Input('refresh-url-statistics', 'n_clicks')],
              events=[Event('interval-component-5', 'interval')])
def refresh_url_statistics(n_clicks):
    return urlsettings.load_statistics('scraped')  # Parameter scraped indicates the total scraped of keywords


# Callback for adding URLs to the database
@app.callback(Output('output-container-button', 'children'),
              [Input('urlsubmit', 'n_clicks')],
              [State('input-box', 'value')])
@db_session
def insert_url(n_clicks, value):
    result = select(p for p in Url if p.url == value).count()  # Retrieving the amount of keywords in the database

    if not value:  # If the user has not submitted anything in the input field
        return html.Div('Please insert a value in the input field.',  # Output warning message
                        id='negative_warning')  # Negative style (red)

    elif result != 0:  # Check if the url already exists in the database
        return html.Div('URL already exists in database',  # Output warning message
                        id='negative_warning')  # Negative style (red)
    else:  # If url does not exist yet
        try:  # Trying
            with db_session:
                url_object = Url(
                    url=value,
                    date_added=datetime.now(),
                    priority_scrape=True,
                    priority_scan=True
                )  # Defining an object of class Keyword
                commit()  # Comitting th object (sending it to database)

            return html.Div('URL: {} has been added to the database.'.format(value),  # Output warning message
                            id='positive_warning') # Positive style (green)

        except:
            return html.Div('An unexpected error occurred',  # Output warning message
                            id='negative_warning')  # Negative style (red)


# Callback used for loading the URL table on the URL Settings page
@app.callback(Output('url-table', 'rows'),
              [Input('reload-button', 'n_clicks')])
@db_session
def reload_table(n_clicks):
    results = select(p for p in Url)[:]  # Retrieving all urls from the database

    df = pd.DataFrame(columns=['URL',  # Defining a dataframe
                               'Date Added',
                               'Date Scan',
                               'Date Scrape',
                               'Priority Scrape',
                               'Priority Scan'])

    for result in results:  # For each keyword in the table do:
        if result.priority_scan:  # If the priority_scan column is true
            priorityscan = 'Yes'

        else:  # If not true then say 'No'
            priorityscan = 'No'

        if result.priority_scrape:  # If the priority_scan column is true
            priorityscrape = 'Yes'

        else:  # If not true then say 'No
            priorityscrape = 'No'

        df = df.append({'URL': result.url,
                        'Date Added': result.date_added,
                        'Date Scan': result.date_scanned,
                        'Date Scrape': result.date_scraped,
                        'Priority Scrape': priorityscrape,
                        'Priority Scan': priorityscan}, ignore_index=True)  # Add the record to a dataframe

    return df.to_dict('records')  # Return each record in the dataframe as a dictionary.


#########################
# Content-block settings
#########################


# Loading the value of StatisticsBox one - total amount of active blockrules in the database
@app.callback(Output('BlockStatisticsBox1', 'children'),
              [Input('refresh-block-statistics', 'n_clicks')],
              events=[Event('interval-component-30', 'interval')])
def refresh_url_statistics(n_clicks):
    return blocksettings.load_statistics('total')  # Parameter total indicates the total amount of keywords


# Loading the value of StatisticsBox two - total amount of active url blocks
@app.callback(Output('BlockStatisticsBox2', 'children'),
              [Input('refresh-block-statistics', 'n_clicks')],
              events=[Event('interval-component-30', 'interval')])
def refresh_url_statistics(n_clicks):
    return blocksettings.load_statistics('urltype')  # Parameter scanned indicates the scanned amount of keywords


# Loading the value of StatisticsBox three - total amount of scraped URLs
@app.callback(Output('BlockStatisticsBox3', 'children'),
              [Input('refresh-block-statistics', 'n_clicks')],
              events=[Event('interval-component-30', 'interval')])
def refresh_url_statistics(n_clicks):
    return blocksettings.load_statistics('keywordtype')  # Parameter scraped indicates the total scraped of keywords


# Callback for adding KEYWORDS to the database
@app.callback(Output('output-container-block', 'children'),
              [Input('blocksubmit', 'n_clicks')],
              [State('block-input-box', 'value'),
               State('block-category', 'value')])
@db_session
def insert_keyword(n_clicks, value, typevalue):
    result = select(p for p in Block if p.value == value and p.type == typevalue).count() # Retrieving the amount

    if not value:  # If the user has not submitted anything in the input field
        return html.Div('Please insert a value in the input field.',  # Output warning message
                        id='negative_warning')  # Negative style (red)

    elif result != 0:  # Check if the keyword already exists in the database
        return html.Div('Value with type already exists in database',  # Output warning message
                        id='negative_warning')  # Negative style (red)

    else:  # If keyword does not exist yet
        try:  # Trying
            keyword_object = Block(
                type=typevalue,
                value=value,
                active=True
            )  # Defining an object of class Keyword
            commit()  # Committing the object (sending it to database)

            return html.Div('Rule: {} of type {} has been added to the database.'.format(value, typevalue),
                            id='positive_warning')  # Positive style (green)

        except:
            return html.Div('An unexpected error occurred',  # Output warning message
                            id='negative_warning')  # Negative style (red)


# Callback used for loading the KEYWORD table on the KEYWORD Settings page
@app.callback(Output('block-table', 'rows'),
              [Input('reload-button', 'n_clicks')])
@db_session
def reload_table(n_clicks):
    results = select(p for p in Block)[:]  # Retrieving all keywords from the database

    global df  # Defining a global dataframe so the keywords can be loaded from the keywords search page

    df = pd.DataFrame(columns=['Type',  # Defining a dataframe with the columns: keyword and status
                               'Value',
                               'Status'])

    for result in results:  # For each keyword in the table do:
        if result.active:  # If the active column is true, then set status equal to the word Active
            status = 'Active'

        else:  # If not active then say Inactive
            status = 'Inactive'

        df = df.append({'Type': result.type,
                        'Value': result.value,
                        'Status': status},
                       ignore_index=True)  # Add the record to a dataframe which can then be displayed in the table

    return df.to_dict('records')  # Return each record in the dataframe as a dictionary.


# Callback for turning KEYWORDS ACTIVE
@app.callback(Output('block_activate_warning', 'children'),
              [Input('block_set_active', 'n_clicks')],
              [State('block-table', 'selected_row_indices')])
@db_session
def insert_url(n_clicks, selected_row_indices):
    try:  # Try changing, if anything goes wrong, a warning message will be displayed instead of an application crash
        if 'df' not in globals():  # Check if the table is loaded
            return html.Div('Please load the blockrule table first.',  # Warning message
                            id='negative_warning')  # Red style (error style)

        elif not selected_row_indices:  # If there are no rows selected
            return html.Div('Please select a blockrule.',  # Warning message
                            id='negative_warning')  # Red style (error style)

        else:
            records = df.iloc[selected_row_indices, :]  # Retrieve the selected rows from the dataframe variable

            for index, row in records.iterrows():
                results = select(p for p in Block if p.value == row['Value'] and p.type == row['Type'])

                for result in results:  # This needs to be unwrapped because the result is a ponyORM object.
                    result.active = True  # Setting the active field to true
                    commit()  # Committing the action

            return html.Div('The selected records are set active.',  # Warning message
                            id='positive_warning')  # Green style (positive style)

    except: # If anything unexpected occurs
        return html.Div('An unexpected error occurred.',  # Warning messsage
                        id='negative_warning')  # Red style (error style)


# Callback for turning KEYWORDS INACTIVE
@app.callback(Output('block_inactivate_warning', 'children'),
              [Input('block_set_inactive', 'n_clicks')],
              [State('block-table', 'selected_row_indices')])
@db_session
def insert_url(n_clicks, selected_row_indices):
    if 'df' not in globals():  # Check if the table is loaded
        return html.Div('Please load the blockrule table first.',  # Warning message
                        id='negative_warning')  # Red style (error style)

    elif not selected_row_indices:  # If there are no rows selected
        return html.Div('Please select a blockrule.',  # Warning message
                        id='negative_warning')  # Red style (error style)

    else:
        records = df.iloc[selected_row_indices, :]  # Retrieve the selected rows from the dataframe variable

        for index, row in records.iterrows():
            results = select(p for p in Block if p.value == row['Value'] and p.type == row['Type'])

            for result in results:  # This needs to be unwrapped because the result is a ponyORM object.
                result.active = False  # Setting the active field to false
                commit()  # Comitting the action

        return html.Div('The selected records are set inactive.',  # Warning message
                        id='positive_warning')  # Green style (positive style)


################
# User Guide settings
################


# Callback used for displaying an controlling the USER GUIDE tabs
@app.callback(Output('tab-output', 'children'),
              [Input('tabs', 'value')])
def display_content(value):
    if value == 1:
        return html.Div([
            dcc.Markdown('''
#### Start
Welcome at the User Guide. This guide provides you inside in how the application works and why certain 
development choices were made. Please use the tabs to navigate to the right guide and get familiar with 
HIVE quickly. 

HIVE is made by team FOUR. on behalf of the Hogeschool van Amsterdam. This application comes with no 
warrenty as stated in the EULA (MIT license).'''),
        ])

    elif value == 2:
        return html.Div([
            dcc.Markdown(''' 
#### URL Settings
On the  [**URL Settings** page](/pages/urlsettings), you are able to view the following sections:

###### Statistics
The statistics provide you with insight in the amount of URLs in the database and the percentage of scaned and
scraped URLs. The button **REFRESH STATISTICS** can be used to refresh the statistics. The application does
not automatically perform tasks such as refreshing or loading information to make the application as fast 
as possible. The statistics are also automatically loaded when the application is started. 

###### Add URLs
You can add URLs to the database by entering a value in the field which says: *URL* which need to be added to
the database. Use the **SUBMIT** button to commit the value and add it to the database. The application
automatically checks whether the URL already exists or not. Added URLs will automatically receive the
Priority Scrape and Priority Scan flag. 

###### Load table
The table is not loaded by default, this done because this can take a while depending on the amount of URLs 
in the database. When using the **LOAD TABLE** button, the application will try to retrieve *all* URLs in
the database. When the application is loading the table, you will not be able to perform other tasks. '''),
        ])

    elif value == 3:
        return html.Div([
            dcc.Markdown(''' 
#### Keyword Settings
On the  [**Keyword Settings** page](/pages/keywordsettings), you are able to view the following sections:

###### Statistics
The statistics provide you with insight in the amount of Keywords in the database and the percentage of active keywords.
The button **REFRESH STATISTICS** can be used to refresh the statistics. The application does
not automatically perform tasks such as refreshing or loading information to make the application as fast 
as possible. The statistics are also automatically loaded when the application is started. 

###### Add Keywords
You can add Keywords to the database by entering a value in the field which says: *Keyword* which need to be added to
the database. Use the **SUBMIT** button to commit the value and add it to the database. The application
automatically checks whether the Keyword already exists or not. Added Keywords will be set active by default. 

###### Load table
The table is not loaded by default, this done because this can take a while depending on the amount of Keywords 
in the database. When using the **LOAD TABLE** button, the application will try to retrieve *all* Keywords in
the database. When the application is loading the table, you will not be able to perform other tasks. 

###### Filter table
By using the **FILTER ROWS** button, you are able to show fields which can be used to filter information in the table. 
 
###### Active/Inactive
The active and inactive buttons can be used to set keywords active or inactive. Inactive keywords will not be matched
any longer but won't be removed from the database as well. As a user, you will still be able to search for content that 
was matched before you set the keyword inactive.'''),
        ])

    elif value == 4:
        return html.Div([
            dcc.Markdown(''' 
#### Content Block Settings
On the [**Keyword Settings** page](/pages/blocksettings), you are able to view the following sections:


###### Statistics
The statistics provide you with insight in the amount of Block-rules in the database and the percentage of active rules.
The button **REFRESH STATISTICS** can be used to refresh the statistics. The application does
not automatically perform tasks such as refreshing or loading information to make the application as fast 
as possible. The statistics are also automatically loaded when the application is started. 

###### Add Rules
You can add Rules to the database by entering a value in the input-field the database. Select the type of rule and use 
the *SUBMIT* button to commit the value and add it to the database. The applicationautomatically checks whether the 
Rule with the specified type already exists or not. Added Rules will be set active 
by default. 

**Keyword type**
The keyword type can be used to block content from the database which contains certain (illegal) information (words).
One a page contains the keyword, the entire page is dropped and is not added to the database. 

**URL type**
The URL type can be used to block certain URLs form being accessed by the crawler (bee) and stored by the scout. Once
a URL matches or contains the specified URL, the URL is being ignored 


###### Load table
The table is not loaded by default, this done because this can take a while depending on the amount of Rules 
in the database. When using the **LOAD TABLE** button, the application will try to retrieve *all* Rules in
the database. When the application is loading the table, you will not be able to perform other tasks. 

###### Filter table
By using the **FILTER ROWS** button, you are able to show fields which can be used to filter information in the table. 
 
###### Active/Inactive
The active and inactive buttons can be used to set Rules active or inactive. Inactive keywords will not be matched
any longer but won't be removed from the database as well. As a user, you will still be able to search for content that 
Rules'''),
        ])

    else:
        return html.Div([
            "An unexpected error occurred."
        ])


###################################################################################
# Application callbacks
#
# This block contains all callbacks which are not related to a specific type of
# page but instead support the entire interface.
###################################################################################


# Callback for displaying and closing the EULA
@app.callback(Output('TermsBoxArea', 'children'),
              [Input('TermsButton', 'n_clicks')],
              [State('TermsBoxArea', 'children')],
              [Event('closeTerms', 'click')])
def open_termsbox(n_clicks, state):
    if state is None and n_clicks != 0:
        return eula.hive_termsofuse

    else:
        return None


# Callback which returns the page-layout based on the pathname of the visited page.
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if (pathname == '/pages/start') or (pathname is None) or (pathname == '/'):  # If the pathname is not equal to path
        return start.layout  # Return the start page

    elif pathname == '/pages/search':  # If the page is equal to search
        return search.layout  # Return the search page

    elif pathname == '/pages/keywordsearch':  # If the page is equal to keyword search
        return keywordsearch.layout  # Return the keyword search page

    elif pathname == '/pages/settings':  # If the page is equal to settings
        return settings.layout  # Return the settings page

    elif pathname == '/pages/urlsettings':  # If the page is equal to urlsettings
        return urlsettings.layout  # Return the urlsettings page

    elif pathname == '/pages/keywordsettings':  # If the page is equal to keywordsettings
        return keywordsettings.layout  # Return the keywordsettings page

    elif pathname == '/pages/blocksettings':
        return blocksettings.layout

    elif pathname == '/pages/configurationsettings':
        return configurationsettings.layout

    elif pathname == '/pages/userguide':
        return userguide.layout

    elif pathname.startswith('/pages/results'):  # If the detailed results page is retrieved with an ID
        try:
            index = int(pathname.split('$', 1)[1])
            resultsid = df.iloc[index]['id']
            domain = df.iloc[index]['Domain']
            keywords = df.iloc[index]['Keywords']
            lastscraped = df.iloc[index]['Last Scraped Date']
            content = df.iloc[index]['Content']

            results = html.Div([
                html.H4('Detailed results'),
                html.A("Back to results",
                       href="javascript:history.back()",
                       className="back_button"),

                html.Div([
                    html.Div([
                        html.H5("Details"),
                        html.Div([
                            html.P("Result ID: ", className="hive_bold"),
                            html.Div(resultsid, className="hive_normal")],
                            id="results_row"),

                        html.Div([
                            html.P("Domain: ", className="hive_bold"),
                            html.Div(domain, className="hive_normal")],
                            id="results_row"),

                        html.Div([
                            html.P("Keywords: ", className="hive_bold"),
                            html.Div(", ".join(keywords), className="hive_normal")],
                            id="results_row"),

                        html.Div([
                            html.P("Last scraped: ", className="hive_bold"),
                            html.Div(lastscraped, className="hive_normal")],
                            id="results_row")
                    ], className="pane"),

                html.Div([
                    html.H5("Content"),
                    html.Div(content, id="results_row")], className="pane")],
                    className="results_dashboard")
            ])

        except:
            results = html.Div(["An unexpected error occurred."])

        return results

    elif pathname.startswith('/pages/search_results'):  # If the detailed results page is retrieved with an ID
        try:
            index= int(pathname.split('$', 1)[1])
            resultsid = df.iloc[index]['id']
            domain = df.iloc[index]['Domain']
            lastscraped = df.iloc[index]['Last Scraped Date']
            content = df.iloc[index]['Content']

            results = html.Div([
                html.H4('Detailed results'),
                html.A("Back to results",
                       href="javascript:history.back()",
                       className="back_button"),

                html.Div([
                    html.Div([
                        html.H5("Details"),
                        html.Div([
                            html.P("Result ID: ", className="hive_bold"),
                            html.Div(resultsid, className="hive_normal")],
                            id="results_row"),

                        html.Div([
                            html.P("Domain: ", className="hive_bold"),
                            html.Div(domain, className="hive_normal")],
                            id="results_row"),

                        html.Div([
                            html.P("Last scraped: ", className="hive_bold"),
                            html.Div(lastscraped, className="hive_normal")],
                            id="results_row")
                    ], className="pane"),

                html.Div([
                    html.H5("Content"),
                    html.Div(dcc.Markdown(str(content)), id="results_row")], className="pane")],
                    className="results_dashboard")
            ])

        except:
            results = html.Div(["An unexpected error occurred."])

        return results

    else:  # Else
        return start.layout  # Return the search page


# Application starting command
if __name__ == '__main__':
    app.run_server(debug=True, host=configuration_get("honeycomb", "ip"))
