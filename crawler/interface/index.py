import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from crawler.models import *
import pandas as pd
import time

# Load pages
from interface.pages import start
from interface.pages import search
from interface.pages import urlsettings
from interface.pages import about
from interface.pages import settings
from interface.pages import keywordsettings

# Load elements
from interface.elements import header

app = dash.Dash()
app.css.append_css({'external_url': 'https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/_layouts/15/guestaccess.aspx?docid=1a328c2860b4b4e66b806b1b92ff5a8b2&authkey=ASrYUvcKKW1vlc60Pe1O3Cc'})
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})
server = app.server
app.config.supress_callback_exceptions = True


app.title = "HIVE - A Dark Web Crawler"
app.layout = html.Div([
    header.hive_header,
    dcc.Location(id='url', refresh = False),
    html.Div(id='page-content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),

])


# Callback used for adding a URL to the database from within the URL-settings page
@app.callback(
    Output('output-container-keyword', 'children'),
    [Input('keywordsubmit', 'n_clicks')],
    [State('keyword-input-box', 'value')])
def insert_keyword(n_clicks, value):
    with db_session:
        result = select(p for p in Keyword if p.keyword == value).count()

    if not value:
        return html.Div('Please insert a value in the input field.',id='negative-warning')
    elif result != 0:
        return html.Div('URL already exists in database',id='negative-warning')
    else:
        try:
            with db_session:
                url_object = Keyword(
                    keyword=value,
                    active=True
                )
                commit()
            return html.Div('Keyword: {} has been added to the database.'.format(value), id='positive-warning')

        except:
            return html.Div('An unexpected error occurred', id='negative-warning')


@app.callback(
    Output('keyword-table', 'rows'),
    [Input('reload-button', 'n_clicks')]
)
@db_session
def reload_table(n_clicks):
    results = select(p for p in Keyword)[:]

    global df
    df = pd.DataFrame(columns=['Keyword', 'Status'])



    for result in results:
        if result.active == True:
            status  = 'Active'

        else:
            status = 'Inactive'


        df = df.append({'Keyword': result.keyword, 'Status': status}, ignore_index=True)

    return df.to_dict('records')

@app.callback(
    Output('inactivate_warning', 'children'),
    [Input('keyword_set_inactive', 'n_clicks')],
    [State('keyword-table', 'selected_row_indices')])
def insert_url(n_clicks, selected_row_indices):
        if not selected_row_indices:
            return html.Div('Please select a keyword.', id='negative-warning')

        else:
            records = df.iloc[selected_row_indices].Keyword

            for record in records:
                print(record)














# Callback used for adding a URL to the database from within the URL-settings page
@app.callback(
    Output('output-container-button', 'children'),
    [Input('urlsubmit', 'n_clicks')],
    [State('input-box', 'value')])
def insert_url(n_clicks, value):
    with db_session:
        result = select(p for p in Url if p.url == value).count()

    if not value:
        return html.Div('Please insert a value in the input field.',id='negative-warning')
    elif result != 0:
        return html.Div('URL already exists in database',id='negative-warning')
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
            return html.Div('URL: {} has been added to the database.'.format(value), id='positive-warning')

        except:
            return html.Div('An unexpected error occurred', id='negative-warning')

@app.callback(
    Output('url-table', 'rows'),
    [Input('reload-button', 'n_clicks')]
)
@db_session
def reload_table(n_clicks):
    results = select(p for p in Url)[:]
    df = pd.DataFrame(columns=['URL', 'Date Added', 'Date Scan', 'Date Scrape', 'Priority Scrape', 'Priority Scan'])

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


# Callback used for displaying the selected page in the layout area of the application
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/start':
        return start.layout
    elif pathname == '/pages/search':
        return search.layout
    elif pathname == '/pages/settings':
        return settings.layout
    elif pathname == '/pages/urlsettings':
        return urlsettings.layout
    elif pathname == '/pages/keywordsettings':
        return keywordsettings.layout
    elif pathname == '/pages/about':
        return about.layout
    else:
        return start.layout













######################################################################
######################################################################
######################################################################
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')