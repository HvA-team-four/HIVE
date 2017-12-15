#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_html_components as html
import dash_core_components as dcc


def user_guide(value):
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

    elif value == 5:

        return html.Div([

            dcc.Markdown(''' 
#### Content Block Settings
On the [**Full-text search** page](/pages/search), you are able to view the following sections:

###### Keywords on user input
The Full-text search engine displays search results on the given keywords. It sorts the results based on the number of keywords
that are found in the text. You can also filter on date. The search engine displays only results based on given keywords and 
the given date.

###### Multiple keywords
For using multiple keywords, a space between the words is needed. For example: first second. The search engine displays 
results based on one of multiple keywords. Results are ranked on on how many keywords are found. 
The results that contains both keywords are high ranked. Results that contains one of the keywords, are lower ranked. 

When you want to get only results based on multiple keywords, you have to specify the keywords with the + character.
For example: +first +second. It displays only results that contains the multiple keywords. The results will ranked on 
amount of keywords that are found. You have also the option to filter on date. 

###### Detail page
When the results are displayed, there is an option to see the detailed page. On the displayed page, the full web page
content is displayed.

'''),])

    else:
        return html.Div([
            "An unexpected error occurred."
        ])


layout = html.Div([
    html.Div([
        html.H3('User guide'),

        html.P('''Use the user guide to find information on how to use HIVE to search through content and to find 
        known issues.'''),

        html.Br(),

        dcc.Tabs(
            tabs=[
                {'label': 'Welcome', 'value': 1},
                {'label': 'URL Settings', 'value': 2},
                {'label': 'Keyword Settings', 'value': 3},
                {'label': 'Content Block Settings', 'value': 4},
                {'label': 'Full-text search', 'value': 5},
            ],
            value=1,
            id='tabs',
            vertical=True,)
    ], className="userguide_menu"),

    html.Div(
        html.Div(id='tab-output'),
        className="userguide_output"
    )
])
