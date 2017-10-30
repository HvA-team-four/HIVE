from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

# Load pages
from app import app
from interface.pages import start
from interface.pages import search
from interface.pages import settings
from interface.pages import about

# Load elements
from interface.elements import header
app.layout = html.Div([
    header.hive_header,
    dcc.Location(id='url', refresh = False),
    html.Div(id='page-content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/start':
        return start.layout
    elif pathname == '/pages/search':
        return search.layout
    elif pathname == '/pages/settings':
        return settings.layout
    elif pathname == '/pages/about':
        return about.layout
    else:
        return start.layout


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')