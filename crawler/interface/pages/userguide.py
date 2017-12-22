#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_html_components as html
import dash_core_components as dcc


def user_guide(value):
    if value == 1:  # Welcome
        # e page
        return html.Div([
            dcc.Markdown('''
#### Start
Welcome at the User Guide. This guide provides you inside in how the application works and why certain 
development choices were made. Please use the tabs to navigate to the right guide and get familiar with 
HIVE quickly. 

HIVE is made by team FOUR. on behalf of the Hogeschool van Amsterdam. This application comes with no 
    warrenty as stated in the EULA (MIT license).'''),
        ])

    elif value == 2:  # Search page
        return html.Div([
            dcc.Markdown(''' 
#### Search
On the [**Full-text search** page](/pages/search), you are able to view the following sections:

###### Keywords on user input
The Full-text search engine displays search results on the given keywords. It sorts the results based on the number of 
keywords that are found in the text. You can also filter on date. The search engine displays only results based on given 
keywords and the given date.

###### Multiple keywords
For using multiple keywords, a space between the words is needed. For example: first second. The search engine displays 
results based on one of multiple keywords. Results are ranked on on how many keywords are found. 
The results that contains both keywords are high ranked. Results that contains one of the keywords, are lower ranked. 

When you want to get only results based on multiple keywords, you have to specify the keywords with the + character.
For example: +first +second. It displays only results that contains the multiple keywords. The results will ranked on 
amount of keywords that are found. You have also the option to filter on date. 

###### Detail page
When the results are displayed, there is an option to see the detailed page. On the displayed page, the full web page
content is displayed.'''),
        ])

    elif value == 3:  # Keyword search page
        return html.Div([
            dcc.Markdown(''' 
#### Keyword Search
Lorum Ipsum dolor sit amet.'''),
        ])

    elif value == 4:  # URL settings
        return html.Div([
            dcc.Markdown(''' 
#### URL Settings
On the  [**URL Settings** page](/pages/urlsettings), you are able to view the following sections:

###### Statistics
The statistics provide you with insight in the amount of URLs in the database and the percentage of scaned and
scraped URLs. The button `Refresh Statistics` can be used to refresh the statistics. The application does
not automatically perform tasks such as refreshing or loading information to make the application as fast 
as possible. The statistics are also automatically loaded when the application is started. 

###### Add URLs
You can add URLs to the database by entering a value in the field which says: *URL* which need to be added to
the database. Use the `Submit` button to commit the value and add it to the database. The application
automatically checks whether the URL already exists or not. Added URLs will automatically receive the
Priority Scrape and Priority Scan flag. 

###### Load table
The table is not loaded by default, this done because this can take a while depending on the amount of URLs 
in the database. When using the `Load Table` button, the application will try to retrieve all URLs in
the database. When the application is loading the table, you will not be able to perform other tasks. '''),
        ])

    elif value == 5:  # Keyword settings
        return html.Div([
            dcc.Markdown(''' 
#### Keyword Settings
On the  [**Keyword Settings** page](/pages/keywordsettings), you are able to view the following sections:

###### Statistics
The statistics provide you with insight in the amount of Keywords in the database and the percentage of active keywords.
The button `Refresh Statistics` can be used to refresh the statistics. The application does
not automatically perform tasks such as refreshing or loading information to make the application as fast 
as possible. The statistics are also automatically loaded when the application is started. 

###### Add Keywords
You can add Keywords to the database by entering a value in the field which says: *Keyword* which need to be added to
the database. Use the `Submit` button to commit the value and add it to the database. The application
automatically checks whether the Keyword already exists or not. Added Keywords will be set active by default. 

###### Load table
The table is not loaded by default, this done because this can take a while depending on the amount of Keywords 
in the database. When using the `Load Table` button, the application will try to retrieve *all* Keywords in
the database. When the application is loading the table, you will not be able to perform other tasks. 

###### Filter table
By using the `Filter Rows` button, you are able to show fields which can be used to filter information in the table. 

###### Active/Inactive
The `Set Active` and `Set Inactive` buttons can be used to set keywords active or inactive. Inactive keywords will not 
be matched any longer but won't be removed from the database as well. As a user, you will still be able to search for 
content that was matched before you set the keyword inactive.'''),
        ])

    elif value == 6:  # Content-block settings
        return html.Div([
            dcc.Markdown(''' 
#### Content Block Settings
On the [**Keyword Settings** page](/pages/blocksettings), you are able to view the following sections:


###### Statistics
The statistics provide you with insight in the amount of Block-rules in the database and the percentage of active rules.
The button `Refresh Statistics` can be used to refresh the statistics. The application does
not automatically perform tasks such as refreshing or loading information to make the application as fast 
as possible. The statistics are also automatically loaded when the application is started. 

###### Add Rules
You can add Rules to the database by entering a value in the input-field the database. Select the type of rule and use 
the `Submit` button to commit the value and add it to the database. The application automatically checks whether the 
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
in the database. When using the `Load Table` button, the application will try to retrieve all Rules in
the database. When the application is loading the table, you will not be able to perform other tasks. 

###### Filter table
By using the `Filter Rows` button, you are able to show fields which can be used to filter information in the table. 

###### Active/Inactive
The `Set Active` and `Set Inactive` buttons can be used to set Rules active or inactive. Inactive keywords will not be 
matched any longer but won't be removed from the database as well. As a user, you will still be able to search for 
content that match those Rules'''),
        ])

    elif value == 7:  # Configuration settings
        return html.Div([
            dcc.Markdown(''' 
#### Configuration Settings
On the [**Configuration Settings** page](/pages/configurationsettings), you are able to view the following sections:


###### File location
The configurations settings page displays the location of the active configuration file on the computer. Please note
that without a configuration file, the application won't start successfully. Make sure to not remove the 
configuration file from the defined location. It is not possible to change the location of the configuration file in
this version of HIVE.

###### Styling
This section displays the location of the css file used for HIVE. This parameter can be changed in the configuration
file. The CSS file needs to be hosted on an external location (a web-server), it is not possible to define a local
CSS file. 

###### Images
This section displays the base path of the image location, the images need to be hosted on an external location
(a web-server). The image folder is distributed in the application folder, make sure to not change the structure of
the image directory.'''),
        ])

    else:
        return html.Div([
            "This User Guide page does not exist yet. "
        ])


# Defining the lay-out of this page.
layout = html.Div([
    html.Div([
        html.H3('User guide'),

        html.P('''Use the user guide to find information on how to use HIVE to search through content and to find 
        known issues.'''),

        html.H5("Usage", style={'margin-top': 20}),
        dcc.Tabs(
            tabs=[
                {'label': 'Welcome', 'value': 1},
                {'label': 'Search', 'value': 2},
                {'label': 'Keyword Search', 'value': 3},
            ],
            id='tabs',
            vertical=True
        ),
        html.H5("Settings", style={'margin-top': 20}),
        dcc.Tabs(
            tabs=[
                {'label': 'URL', 'value': 4},
                {'label': 'Keyword', 'value': 5},
                {'label': 'Content Block', 'value': 6},
                {'label': 'Configuration', 'value': 7},
                {'label': 'User Guide', 'value': 8},
                {'label': 'Search Log', 'value': 9},

            ],
            id='tabs',
            vertical=True,
            value=1
        )
    ], className="userguide_menu"),

    html.Div(
        html.Div(id='tab-output'),
        className="userguide_output"
    )
])
