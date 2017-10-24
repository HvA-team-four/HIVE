import dash_html_components as html
import base64

hive_header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.Img(
                src="https://lh3.googleusercontent.com/Ybh2Nnp3tz7A1hZgE96cNjAATd7kR7Fa9_A4ErsHMz8Pd7aYnUbstj7h4mqGXz398a9wkMtJ2XWOImk=w1686-h1302",
                className="logo"
            ),

            html.Div(className="links", children=[
                html.A('pricing', className="link", href="/pages/start"),
                html.A('workshops', className="link", href="/pages/search")
            ])
        ]
    )
)