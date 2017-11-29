from interface.index import *
import dash_html_components as html
import dash_core_components as dcc
from crawler.utilities.models import *

@db_session
def load_statistics(statistic):
    if statistic == 'total':
        return select(p for p in Keyword).count()

    elif statistic == 'active':
        total = select(p for p in Keyword).count()
        if total != 0:
            active = select(p for p in Keyword if p.active == True ).count()
            percentage = int(active/total*100)
        else:
            percentage = 0
        return '{}%'.format(percentage)

    elif statistic == 'other':
        return '...'

layout = html.Div([
    html.H3('Content Block Settings',
            style={'text-align':'center'}),

    html.P('On this page, the content block settings for HIVE can be set. Blocked content will not be stored in the database and will simply be ignored. Please use the controls to define content which needs to be blocked',
           style={'width':380,
                  'marginLeft':'auto',
                  'marginRight':'auto',
                  'textAlign':'center',
                  'marginBottom':10}),

    html.Div([
            html.Div([
                html.Div(children   = load_statistics('total'),
                         id         = 'BlockStatisticsBox1',
                         className  = 'statisticsBox'),
                html.Div(children   = 'Total',
                         className  = 'title'),
                html.Div(children   = 'Amount of keywords in the database',
                         className  = 'description')
            ], className    = 'statisticsWrapper'),

            html.Div([
                html.Div(children   = load_statistics('active'),
                         className  = 'statisticsBox',
                         id         = 'BlockStatisticsBox2'),
                html.Div(children   = 'Active',
                         className  = 'title'),
                html.Div(children   = 'Percentage of active keywords',
                         className  = 'description')
            ], className    = 'statisticsWrapper'),

            html.Div([
                html.Div(children   = load_statistics('other'),
                         className  = 'statisticsBox',
                         id         = 'BlockStatisticsBox3'),
                html.Div(children   = 'Other',
                         className  = 'title'),
                html.Div(children   = 'No information yet',
                         className  = 'description')
            ], className    = 'statisticsWrapper'),

            html.Button('Refresh statistics',
                        id          = 'refresh-block-statistics',
                        className   = 'refresh_button')
        ], className    = 'statisticsRow'),

        html.Div([
                dcc.Input(id        = 'keyword-input-box',
                          type      = 'text',
                          style     = {'width': 480},
                          placeholder   ='String-match which needs to be blocked'),

                dcc.RadioItems(
                    id='block-category',
                    options=[
                        {'label': 'Keyword', 'value': 'Keyword'},
                        {'label': 'URL', 'value': 'Url'}
                    ],
                    value='Keyword',
                    labelStyle={'display': 'inline-block'}
                ),

                html.Button('Submit',
                            id      = 'keywordsubmit',
                            style   = {'marginLeft': 20}),

                html.Br(),
                html.Br(),

                html.Div(id     = 'output-container-keyword')
            ]),





















])