import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
from dash.dependencies import Input, Output, State

from crawler.models import *
from crawler.utilities import config

# Load elements
from interface.elements import header
from interface.pages import about
from interface.pages import keywordsearch
from interface.pages import search
from interface.pages import settings
# Load pages
from interface.pages import start
from interface.pages import urlsettings
from interface.pages import keywordsettings

app = dash.Dash()
app.css.append_css({'external_url': config.configuration_get("styling", "css")})
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
server = app.server
app.config.supress_callback_exceptions = True


app.title = 'HIVE - A Dark Web Crawler'
app.layout = html.Div([
    header.hive_header,

    dcc.Location(id='url',
                 refresh = False),

    html.Div(id='page-content'),

    html.Div(
        dt.DataTable(rows=[{}]),
        style={'display': 'none'}),
])


#######################################
#################   Keyword Search Page
#######################################
@app.callback(
    Output('keywordList', 'options'),
    [Input('refresh-keyword-list', 'n_clicks')])
def refresh_keyword_list(n_clicks):
    return keywordsearch.load_keywords()

#######################################
###############   Keyword Settings Page
#######################################

# Loading the value of StatisticsBox one
@app.callback(
    Output('KeywordStatisticsBox1', 'children'),
    [Input('refresh-keyword-statistics', 'n_clicks')])
def refresh_keyword_statistics(n_clicks):
    return keywordsettings.load_statistics('total')

# Loading the value of StatisticsBox two
@app.callback(
    Output('KeywordStatisticsBox2', 'children'),
    [Input('refresh-keyword-statistics', 'n_clicks')])
def refresh_keyword_statistics(n_clicks):
    return keywordsettings.load_statistics('active')

# Loading the value of StatisticsBox three
@app.callback(
    Output('KeywordStatisticsBox3', 'children'),
    [Input('refresh-keyword-statistics', 'n_clicks')])
def refresh_keyword_statistics(n_clicks):
    return keywordsettings.load_statistics('other')

# Input for adding Keywords to the database
@app.callback(
    Output('output-container-keyword', 'children'),
    [Input('keywordsubmit', 'n_clicks')],
    [State('keyword-input-box', 'value')])
def insert_keyword(n_clicks, value):
    with db_session:
        result = select(p for p in Keyword if p.keyword == value).count()

    if not value:
        return html.Div('Please insert a value in the input field.',
                        id='negative_warning')

    elif result != 0:
        return html.Div('Keyword already exists in database',
                        id='negative_warning')

    else:
        try:
            with db_session:
                url_object = Keyword(
                    keyword=value,
                    active=True
                )
                commit()

            return html.Div('Keyword: {} has been added to the database.'.format(value),
                            id='positive_warning')

        except:
            return html.Div('An unexpected error occurred',
                            id='negative_warning')

# Loading the Keyword table from the database
@app.callback(
    Output('keyword-table', 'rows'),
    [Input('reload-button', 'n_clicks')])
@db_session
def reload_table(n_clicks):
    results = select(p for p in Keyword)[:]

    global df
    df = pd.DataFrame(columns=['Keyword',
                               'Status'])

    for result in results:
        if result.active == True:
            status  = 'Active'

        else:
            status = 'Inactive'


        df = df.append({'Keyword': result.keyword,

                        'Status': status},
                       ignore_index=True)

    return df.to_dict('records')

# Changing the status of a Keyword to active
@app.callback(
    Output('activate_warning', 'children'),
    [Input('keyword_set_active', 'n_clicks')],
    [State('keyword-table', 'selected_row_indices')])
@db_session
def insert_url(n_clicks, selected_row_indices):
    try:
        if 'df' not in globals():
            return html.Div('Please load the keyword table first.',
                            id='negative_warning')

        elif not selected_row_indices:
            return html.Div('Please select a keyword.',
                            id='negative_warning')

        else:
            records = df.iloc[selected_row_indices].Keyword

            for record in records:
                results = select(p for p in Keyword if p.keyword == record)

                for result in results:
                    result.active = True
                    commit()

            return html.Div('The selected records are set active.',
                            id='positive_warning')


    except:
        return html.Div('An unexpected error occurred.',
                        id='negative_warning')

# Changing the status of a Keyword to inactive
@app.callback(
    Output('inactivate_warning', 'children'),
    [Input('keyword_set_inactive', 'n_clicks')],
    [State('keyword-table', 'selected_row_indices')])
@db_session
def insert_url(n_clicks, selected_row_indices):
    try:
        if 'df' not in globals():
            return html.Div('Please load the keyword table first.',
                            id='negative_warning')

        elif not selected_row_indices:
            return html.Div('Please select a keyword.',
                            id='negative_warning')

        else:
            records = df.iloc[selected_row_indices].Keyword

            for record in records:
                results = select(p for p in Keyword if p.keyword == record)

                for result in results:
                    result.active = False
                    commit()

            return html.Div('The selected records are set inactive.',
                            id='positive_warning')
    except:
        return html.Div('An unexpected error occurred.',
                        id='negative_warning')

#######################################
###################   URL Settings Page
#######################################

# Loading the value of StatisticsBox one
@app.callback(
    Output('UrlStatisticsBox1', 'children'),
    [Input('refresh-statistics', 'n_clicks')])
def refresh_url_statistics(n_clicks):
    return urlsettings.load_statistics('total')

# Loading the value of StatisticsBox two
@app.callback(
    Output('UrlStatisticsBox2', 'children'),
    [Input('refresh-statistics', 'n_clicks')])
def refresh_url_statistics(n_clicks):
    return urlsettings.load_statistics('scanned')

# Loading the value of StatisticsBox three
@app.callback(
    Output('UrlStatisticsBox3', 'children'),
    [Input('refresh-statistics', 'n_clicks')])
def refresh_url_statistics(n_clicks):
    return urlsettings.load_statistics('scraped')

# Input for adding URLs to the database
@app.callback(
    Output('output-container-button', 'children'),
    [Input('urlsubmit', 'n_clicks')],
    [State('input-box', 'value')])
def insert_url(n_clicks, value):
    with db_session:
        result = select(p for p in Url if p.url == value).count()

    if not value:
        return html.Div('Please insert a value in the input field.',
                        id='negative_warning')

    elif result != 0:
        return html.Div('URL already exists in database',
                        id='negative_warning')
    else:
        try:
            with db_session:
                url_object = Url(
                    url=value,
                    date_added=datetime.now(),
                    priority_scrape=True,
                    priority_scan=True
                )
                commit()

            return html.Div('URL: {} has been added to the database.'.format(value),
                            id='positive_warning')

        except:
            return html.Div('An unexpected error occurred',
                            id='negative_warning')

# Loading the URL table from the database
@app.callback(
    Output('url-table', 'rows'),
    [Input('reload-button', 'n_clicks')]
)
@db_session
def reload_table(n_clicks):
    results = select(p for p in Url)[:]
    df = pd.DataFrame(columns=['URL',
                               'Date Added',
                               'Date Scan',
                               'Date Scrape',
                               'Priority Scrape',
                               'Priority Scan'])

    for result in results:
        if result.priority_scan == True:
            priorityscan = 'Yes'

        else:
            priorityscan = 'No'

        if result.priority_scrape == True:
            priorityscrape = 'Yes'

        else:
            priorityscrape = 'No'

        df = df.append({'URL': result.url,
                        'Date Added': result.date_added,
                        'Date Scan': result.date_scanned,
                        'Date Scrape': result.date_scraped,
                        'Priority Scrape': priorityscrape,
                        'Priority Scan': priorityscan}, ignore_index=True)

    return df.to_dict('records')


#######################################
##############   Page Selector Callback
#######################################
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/start':
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
    elif pathname == '/pages/configsettings':
        return configsettings.layout
    elif pathname == '/pages/about':
        return about.layout

    else:
        return start.layout




######################################################################
######################################################################
######################################################################
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')