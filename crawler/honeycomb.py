#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
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
from interface.pages import searchlog
from utilities.models import *
from utilities.config import *
from datetime import datetime
import re

sys.path.append('../')

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


@app.callback(Output('normal_search_results', 'children'),
              [Input('normal_search', 'n_clicks')],
              [State('search_bar', 'value'),
               State('normal_date_picker', 'start_date'),
               State('normal_date_picker', 'end_date')])
def display_results(n_clicks, values, start_date, end_date):
    """This function is called from the search page when a users inputs a query and clicks on the search button.
    The start_date and end_date are inputted as well.
    """
    values_array = (re.findall(r"[\w']+", values))
    search.save_query(values_array, start_date, end_date)  # Save the query in the database (logging)

    global df  # Creating a global variable in which the results will be stored

    # The following function calls the normal_search() function which is located at the
    # Search.py file, it provides the required parameters. Results are stored in the
    # Global dataframe
    df = search.normal_search(values_array, values, start_date, end_date)

    if df.empty:  # Check if the dataframe contains any results
        results = html.Div([
            html.Div([
                html.H4("Results"),
                html.P(  # Display a no results message
                    "No results were found based on your search",
                    style={"width": 370,
                           "marginBottom": 15}),
            ], className="content")
        ], className="results_section")
    else:  # If any results were returned
        results = html.Div([
            html.Div([
                html.H4("Results"),

                html.P('''The following table displays all the search results which were retrieved based 
                on your search query.''',
                       style={"width": 370,
                              "marginBottom": 15}),

                # The following function builds a dynamic HTML table based on the records in the
                # Global dataframe. The entire output-element is stored in the "results" variable
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

    return results  # Return the results, they will be displayed as children in the normal_search_results element.


@app.callback(Output('keywordList', 'options'),
              [Input('refresh-keyword-list', 'n_clicks')],
              events=[Event('interval-component-30', 'interval')])
def refresh_keyword_list(n_clicks):
    """This function loads the keywords table every 30 seconds. This is done because the user is
    able to add new keywords, which of course need to be loaded in order for the user to search
    on them. This function (load_keywords()) is located at the keywordsearch.py file
    """
    return keywordsearch.load_keywords()


@app.callback(Output('keyword_search_results', 'children'),
              [Input('keyword_search', 'n_clicks')],
              [State('keywordList', 'value'),
               State('keyword_date_picker', 'start_date'),
               State('keyword_date_picker', 'end_date')])
def display_results(n_clicks, values, start_date, end_date):
    """This callback is used by the keyword search page when a users inputs a query and clicks on the search
    button. The start_date and end_date can be entered as parameters
    """
    keywordsearch.save_query(values, start_date, end_date)  # Save the query in the database (logging)

    global df  # Creating a global variable in which the results will be stored

    # The following function calls the keyword_search() function which is located at the
    # Keywordsearch.py file, it provides the required parameters. Results are stored in the
    # Global dataframe
    df = keywordsearch.keyword_search(values, start_date, end_date)

    if df.empty: # Check if the dataframe contains any results
        results = html.Div([
            html.Div([
                html.H4("Results"),
                html.P(  # Display a no results message
                    "No results were found based on your keyword search",
                    style={"width": 370,
                           "marginBottom": 15}),
                ], className="content")
            ], className="results_section")
    else:  # If any results were returned
        results = html.Div([
            html.Div([
                html.H4("Results"),
                html.P('''The following table displays all the search results which were retrieved based 
                on your search query.''',
                       style={"width": 370,
                              "marginBottom": 15}),

                # The following function builds a dynamic HTML table based on the records in the
                # Global dataframe. The entire output-element is stored in the "results" variable
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

    return results  # Return the results, they will be displayed as children in the keyword_search_results element.


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


@app.callback(Output('output-container-keyword', 'children'),
              [Input('keywordsubmit', 'n_clicks')],
              [State('keyword-input-box', 'value')])
@db_session
def insert_keyword(n_clicks, value):
    """This callbacks add keywords to the database and is called from the keyword settings page when a user clicks the
    submit button. The entered keyword is stored in the database and a message will be displayed.
    """
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


@app.callback(Output('keyword-table', 'rows'),
              [Input('reload-button', 'n_clicks')])
@db_session
def reload_table(n_clicks):
    """This callback is used to load the keyword table on the keyword settings page. The function is called when
    the user clicks on the load_table button.
    """
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


@app.callback(Output('activate_warning', 'children'),
              [Input('keyword_set_active', 'n_clicks')],
              [State('keyword-table', 'selected_row_indices')])
@db_session
def keywords(n_clicks, selected_row_indices):
    """This callback is used to set keywords active. This function is triggered by a user when a rule is selected
    and the user clicks on 'set active'.
    """
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


@app.callback(Output('inactivate_warning', 'children'),
              [Input('keyword_set_inactive', 'n_clicks')],
              [State('keyword-table', 'selected_row_indices')])
@db_session
def keywords(n_clicks, selected_row_indices):
    """This callback is used to set keywords inactive. This function is triggered by a user when a rule is selected
    and the user clicks on 'set inactive'.
    """
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


@app.callback(Output('output-container-button', 'children'),
              [Input('urlsubmit', 'n_clicks')],
              [State('input-box', 'value')])
@db_session
def insert_url(n_clicks, value):
    """This callbacks add URLs to the database and is called from the URLsettings page when a user clicks the
    submit button. The entered url is stored in the database and a message will be displayed.
    """
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


@app.callback(Output('url-table', 'rows'),
              [Input('reload-button', 'n_clicks')])
@db_session
def reload_table(n_clicks):
    """This callback loads the URL-table when a users clicks the Load Table button on the URL settings page
    the function retrieves all URLs from the database.
    """
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


@app.callback(Output('output-container-block', 'children'),
              [Input('blocksubmit', 'n_clicks')],
              [State('block-input-box', 'value'),
               State('block-category', 'value')])
@db_session
def insert_keyword(n_clicks, value, typevalue):
    """This callback adds a keyword to the keyword-table in the database when a user clicks on submit. The callback
    contains a warning mechanism, warnings are displayed in the output-container-block.
    """
    result = select(p for p in Block if p.value == value and p.type == typevalue).count()  # Retrieving the amount

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


@app.callback(Output('block-table', 'rows'),
              [Input('reload-button', 'n_clicks')])
@db_session
def content_block(n_clicks):
    """This callback is used to load the table with blockrules. The function is triggered when a user clicks
    on the 'load table' button on the Content Block Settings page.
    """
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


@app.callback(Output('block_activate_warning', 'children'),
              [Input('block_set_active', 'n_clicks')],
              [State('block-table', 'selected_row_indices')])
@db_session
def content_block(n_clicks, selected_row_indices):
    """This callback is used to set blockrules active. This function is triggered by a user when a rule is selected
    and the user clicks on 'set active'.
    """
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


@app.callback(Output('block_inactivate_warning', 'children'),
              [Input('block_set_inactive', 'n_clicks')],
              [State('block-table', 'selected_row_indices')])
@db_session
def content_block(n_clicks, selected_row_indices):
    """This callback is used to set blockrules inactive. This function is triggered by a user when a rule is selected
    and the user clicks on 'set inactive'.
    """
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


#####################
# User Guide settings
#####################


@app.callback(Output('tab-output', 'children'),
              [Input('tabs', 'value')])
def display_content(value):
    """This callback is used on the User Guide page and returns the selected User Guide when a user selects
    a certain tab. User Guides can be added to HIVE in the userguide.py page.
    """
    return userguide.user_guide(value)

#####################
# Search Log
#####################


@app.callback(Output('searchlog-table', 'rows'),
              [Input('reload-button', 'n_clicks')])
@db_session
def reload_table(n_clicks):
    """Callback which is used for loading the Search Log table, this callback is triggered when the user clicks on the
    load table button on the Search Log settings page.
    """
    results = select(p for p in Search).order_by(desc(Search.date_searched))[:]  # Retrieving all urls from the database

    df = pd.DataFrame(columns=['Query',  # Defining a dataframe
                               'Date Searched'])

    for result in results:  # For each keyword in the table do:
        df = df.append({'Query': result.query,
                        'Date Searched': result.date_searched}, ignore_index=True)  # Add the record to a dataframe

    return df.to_dict('records')  # Return each record in the dataframe as a dictionary.


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
    """Callback which displays the EULA box when clicking on the LICENSE AGREEMENT button in the bottom bar.
    The EULA is located at the EULA.py file.
        """
    if state is None and n_clicks != 0:
        return eula.hive_termsofuse

    else:
        return None


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """Callback which returns the page-layout based on the pathname of the visited page. For example, when visiting
    the URL: /pages/search, the layout element from the search function is returned.
    """
    if (pathname == '/pages/start') or (pathname is None) or (pathname == '/'):
        return start.layout

    elif pathname == '/pages/search':
        return search.layout

    elif pathname == '/pages/keywordsearch':
        return keywordsearch.layout

    elif pathname == '/pages/settings':
        return settings.layout

    elif pathname == '/pages/urlsettings':
        return urlsettings.layout

    elif pathname == '/pages/keywordsettings':
        return keywordsettings.layout

    elif pathname == '/pages/blocksettings':
        return blocksettings.layout

    elif pathname == '/pages/configurationsettings':
        return configurationsettings.layout

    elif pathname == '/pages/userguide':
        return userguide.layout

    elif pathname == '/pages/searchlog':
        return searchlog.layout

    elif pathname.startswith('/pages/results'):
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

    else:
        return start.layout


# Application starting command
if __name__ == '__main__':
    app.run_server(debug=True, host=configuration_get("honeycomb", "ip"))
