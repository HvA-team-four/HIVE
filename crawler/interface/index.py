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
html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.Img(
                src="https://lh3.googleusercontent.com/Ybh2Nnp3tz7A1hZgE96cNjAATd7kR7Fa9_A4ErsHMz8Pd7aYnUbstj7h4mqGXz398a9wkMtJ2XWOImk=w1686-h1302",
                className="logo"
            ),

            html.Div(className="links", children=[
                html.A('pricing', className="link", href="/pages/start"),
                html.A('workshops', className="link", href="/pages/search")
            ])
        ]
    )
),

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