from interface.index import *

df = pd.DataFrame(columns=['Keyword Table'])
df = df.append({'Keyword Table': "Please load table"}, ignore_index=True)


layout = html.Div([
    html.H3('Keyword Settings'),
    html.P('On this page, you are able to add and remove Keywords to/from the database.', style={'width':380}),
    html.Button('Load table', id='reload-button', style={'marginLeft':20, 'float':'right'}),

    html.Div([
        dcc.Input(id='keyword-input-box', type="text", style={'width': 480}, placeholder='Keyword which need to be added to the database.'),
        html.Button('Submit', id='keywordsubmit', style={'marginLeft': 20}),


    html.Br(),html.Br(),
        html.Div(id='output-container-keyword', children="")]),


    html.Br(),
    html.Div(dt.DataTable(rows=df.to_dict('records'),
        sortable = True,
        row_selectable=True,
        filterable=True,
        selected_row_indices=[],
        id = 'keyword-table')
    ),
    html.Button('Set inactive', id='keyword_set_inactive', style={'marginTop': 20}),
    html.Br(), html.Br(),
    html.Div(id='inactivate_warning', children="")
])
