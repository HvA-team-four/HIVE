import dash_html_components as html

layout = html.Div([
    html.H3('Settings'),
    html.A("URL Settings", href="urlsettings"),
    html.A("Keyword Settings", href="keywordsettings")
])