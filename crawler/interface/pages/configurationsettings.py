from interface.honeycomb import *
import dash_html_components as html
import dash_core_components as dcc
from crawler.utilities.models import *
from crawler.utilities.config import *


configlocation = location_configuration()
csslocation = configuration_get("styling", "css")

df = pd.DataFrame(columns=['Type', 'Value', 'Status'])
df = df.append({'Type': 'No data loaded'}, ignore_index=True)

layout = html.Div([
    html.H3('Configuration Settings',
            style={'text-align':'center'}),

    html.P('On this page, The values in the configuration file can be read and set. Also, the location of the configuration file and the status are displayed.',
           style={'width':380,
                  'marginLeft':'auto',
                  'marginRight':'auto',
                  'textAlign':'center',
                  'marginBottom':10}),

    html.H4('Configuration file'),
    html.P('Location of the configuration file:',
           style={'width':380,
                  'marginBottom':2}),
    html.P(configlocation, style={"fontWeight" : "bold"}),
    html.Br(),

    html.H4('Styling'),
    html.P('Location of the CSS file:',
           style={'width':380,
                  'marginBottom':2}),
    html.P(csslocation, style={"fontWeight" : "bold", "width" : 800, "wordWrap" : "breakWord"})










  ])