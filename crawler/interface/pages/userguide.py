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
#### Full text-search
On the [**Full-text search** page](/pages/search), you are able to view the following sections:

###### Multiple keywords
For using multiple keywords, a space between the words is needed. For example: `apple banana`. 

###### Specific search
You can specify different operators to perform a specific search:

**apple banana**\n
find rows that contain at least one of the two words.

**+apple +juice**\n
Find rows that contain both words (`apple` and `juice`)

**+apple macintosh**\n
Find rows that contain the word `apple`, but rank rows higher if they also contain `macintosh`.

**+apple -macintosh**\n
Find rows that contain the word `apple` but not `macintosh`.

**+apple ~macintosh**\n
Find rows that contain the word `apple`, but if the row also contains the word `macintosh`, 
rate it lower than if row does not. This is `softer` than a search for '+apple -macintosh', 
for which the presence of `macintosh` causes the row not to be returned at all.

**+apple +(>turnover <strudel)**\n
Find rows that contain the words `apple` and `turnover`, or `apple` and `strudel` (in any order), 
but rank `apple turnover` higher than `apple strudel`.

**apple**\n
Find rows that contain words such as `apple`, `apples`, `applesauce` or `applet`.

**"some words"**\n
Find rows that contain the exact phrase `some words` (for example, rows that contain `some words of wisdom` but not 
`some noise words`). Note that the " characters that enclose the phrase are operator characters that delimit the phrase.
They are not the quotation marks that enclose the search string itself.\n

###### Ranking on result
The ranking of results depends on which operator are you using. 
The ranking formula is as follow:

TF-IDF is a numerical statistic that is intended to reflect how important a word is.

IDF: the total number of websites divided by that number of websites that the search term appears in. 
TF: amount that search term appears in text of website

Formula is TF * IDF * IDF

###### Detail page
When the results are displayed, there is an option to see the detailed page. On the displayed page, the full web page
content is displayed.'''),
        ])

    elif value == 3:  # Keyword search page
        return html.Div([
            dcc.Markdown('''
#### Keyword Search 
On the [**Keyword Search** page](/pages/keywordsearch), you are able to view the following sections:

###### Select Keywords
The select keywords bar allows you to select **active** keywords from the keywords table in the database. When adding 
new keywords on the settings page, this list needs to be updated, please use the `Reload Keywords` button ot reload the 
list of keywords. 

###### Multiple Keywords
When selecting multiple keywords, results are returned which match both of the keywords. When searching, for example, on 
'HIVE' en 'Injection', the application returns all results with both of these keywords. 

###### Start and end date
The start and end date fields can be used to define the range of the scraped pages. When defining a range, only the 
results scraped in this range are returned. When defining no date-range, all matching results are returned. 

###### Detail page
When the results are displayed, there is an option to see the detailed page. On the displayed page, the full web page
content is displayed.
'''),
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

    elif value == 8:  # User Guide
        return html.Div([
            dcc.Markdown(''' 
#### User Guide
In the [**User Guide** ](/pages/userguide), you are able to view help documentation about HIVE and you are able to 
get to know the features of the application. Please read the User Guide at least one time before using the application 
in a production environment.
        '''),
        ])

    elif value == 9:  # Search Log
        return html.Div([
            dcc.Markdown(''' 
#### Search Log
In the [**Search Log** ](/pages/searchlog), you are able to view the following sections:

###### Search Log Table
The search log table shows all search requests that have been made using the honeycomb (interface). When searching for
a specific query, the query including all parameters (start-date, end-date) are combined and stored in the database. 

The timestamp of the search is stored as well.

It is not possible to delete the search log (only an administrator can).

###### Filter Rows
The filter rows button can be used to filter rows in the search log. For example, when you are looking for a specific 
search, you can use this button.
    '''),
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
], style={'overflow': 'auto'})
