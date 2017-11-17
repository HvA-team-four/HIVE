import dash_html_components as html

layout = html.Div(style={'textAlign' : 'center'}, children=[
    html.Img(
        src="https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/Documents/HIVE/Images/HIVE.png?slrid=6714269e-8031-4000-938d-c9e3003f7c2c",
        style={'width' : 260, 'marginLeft' : 'auto', 'marginRight' : 'auto', 'marginTop' : 100}),
    html.P("VERSION 2.0 (Development Béta)", className="hive_bold"),
    html.P(style={'maxWidth' : 400, 'marginLeft' : 'auto', 'marginRight' : 'auto'}, children=[
        "Welcome at HIVE. HIVE is a Dark Web Crawler which can be used to crawl the Dark Web and store content in a encrypted database."
    ]),
    html.A('View about page', className="", href="/pages/about")
])
