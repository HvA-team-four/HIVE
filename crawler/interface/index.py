from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from crawler.models import *

# Load pages
from app import app
from interface.pages import start
from interface.pages import search
from interface.pages import urlsettings
from interface.pages import about

# Load elements
from interface.elements import header
app.layout = html.Div([
    header.hive_header,
    dcc.Location(id='url', refresh = False),
    html.Div(id='page-content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),

])

@app.callback(
    Output('output-container-button', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')])
def update_output(n_clicks, value):
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












@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/start':
        return start.layout
    elif pathname == '/pages/search':
        return search.layout
    elif pathname == '/pages/urlsettings':
        return urlsettings.layout
    elif pathname == '/pages/about':
        return about.layout
    else:
        return start.layout


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')