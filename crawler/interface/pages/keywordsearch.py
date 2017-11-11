from interface.index import *
from dash.dependencies import  Input, Output
import dash_html_components as html
import dash_core_components as dcc

@db_session
def load_keywords():
    results = select(p for p in Keyword if p.active == True)[:]

    df = pd.DataFrame(columns=['label',
                               'value'])

    for result in results:
        df = df.append({'label': result.keyword,
                        'value': result.keyword},
                   ignore_index=True)

    return df.to_dict('records')


layout = html.Div([
    html.H3('Keyword Search',
            style={'text-align':'center',
                   'marginTop': 50}),

    html.P('Please use the dropdown-bar below to select the keywords you want to search the database for.',
           style={'width':380,
                  'marginLeft':'auto',
                  'marginRight':'auto',
                  'textAlign':'center',
                  'marginBottom':30}),

    html.Div([
    html.Div([
        dcc.Dropdown(
            options=load_keywords(),
            multi=True,
            id='keywordList',
        )
    ]),
    html.Br(),
    dcc.DatePickerRange(
        id='keyword_date_picker',
        start_date_placeholder_text='Start date',
        end_date_placeholder_text='End date'
    ),
html.Button('Search', id='keyword_search'),
    html.Button('Reload keywords',
                        id          = 'refresh-keyword-list',
                        className   = 'refresh_button',
                        style       = {'paddingLeft' : 10,
                                       'paddingRight' : 10})

    ], style={'width':700, 'marginLeft':'auto', 'marginRight':'auto'})



])