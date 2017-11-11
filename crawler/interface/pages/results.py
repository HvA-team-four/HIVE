from interface.index import *
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

df = pd.DataFrame(columns=['id',
                           'Domain',
                           'Keywords',
                           'Last Scraped Date',
                           'Content'])

df = df.append({'id': 1,
                'Domain':'asdfasdfkjalsdk.onion',
                'Keywords':['Hello', 'Twenty'],
                'Last Scraped Date':'11-12-2017',
                'Content':'Hi how are you doing'},
               ignore_index=True)


def generate_table(dataframe):
     return html.Table(

         [html.Tr([

             html.Div(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in min(len(dataframe))]
    )



layout = html.Div(children=[
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)