import dash_html_components as html # Importing Dash HTML components as html
import dash_core_components as dcc

layout = html.Div([
    html.Div([
        html.H3('User guide'),
        html.P('Use the user guide to find information on how to use HIVE to search through content and to find known issues.'),
        html.Br(),
        dcc.Tabs(
            tabs=[
                {'label': 'Start', 'value': 1},
                {'label': 'Purpose', 'value': 2},
                {'label': 'Settings', 'value': 3},
                {'label': 'Keyword Search', 'value': 4},
            ],
            value=3,
            id='tabs',
            vertical=True,
        )],
        className="userguide_menu"),

    html.Div(
        html.Div(id='tab-output'),
        className="userguide_output"
    )
])



