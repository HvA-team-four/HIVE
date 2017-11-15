from interface.index import *
import dash_html_components as html
import dash_core_components as dcc

layout = html.Div([
    html.H3('Search',
            style={'text-align':'center',
                   'marginTop': 50}),

    html.P('Please use input field below to specify a search query.',
           style={'width':380,
                  'marginLeft':'auto',
                  'marginRight':'auto',
                  'textAlign':'center',
                  'marginBottom':30}),

    html.Div([
        dcc.Input(
            placeholder='Please enter a search query...',
            id='search_bar',
            required=True
        ),
    html.Br(),
    dcc.DatePickerRange(
        id='normal_date_picker',
        start_date_placeholder_text='Start date',
        end_date_placeholder_text='End date'
    ),
    html.Button('Search', id='normal_search', style={'float':'right', 'marginRight': -20})

    ], style={'width':700, 'marginLeft':'auto', 'marginRight':'auto'})



])