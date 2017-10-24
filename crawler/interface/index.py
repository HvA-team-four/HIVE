from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# Load pages
from app import app
from interface.pages import start
from interface.pages import search

# Load elements
from interface.elements import header

app.layout = html.Div([
    header.hive_header,
    dcc.Location(id='url', refresh = False),
    html.Div(id='page-content')
])

my_css_url = "https://raw.githubusercontent.com/HvA-team-four/HIVE/DashInterface/crawler/interface/assets/hive.css"
app.css.append_css({
    "external_url": my_css_url

})

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/start':
        return start.layout
    elif pathname == '/pages/search':
        return search.layout
    else:
        return start.layout


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')