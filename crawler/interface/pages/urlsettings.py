from interface.index import *

df = pd.DataFrame(columns=['URL Table'])
df = df.append({'URL Table': "Please load table"}, ignore_index=True)


layout = html.Div([
    html.H3('URL Settings'),
    html.P('On this page, you are able to add URLs to the database which will automatically receive a priority flag', style={'width':380}),
    html.Button('Load table', id='reload-button', style={'marginLeft':20, 'float':'right'}),

    html.Div([
        dcc.Input(id='input-box', type="text", style={'width': 480}, placeholder='URL which need to be added to the database.'),
        html.Button('Submit', id='urlsubmit', style={'marginLeft': 20}),


    html.Br(),html.Br(),
        html.Div(id='output-container-button', children="")]),


    html.Br(),
    html.Div(dt.DataTable(rows=df.to_dict('records'),
        sortable = True,
        id = 'url-table')
    ),
])