import dash_html_components as html # Importing Dash HTML components as html
from crawler.utilities.config import *

hive_header = html.Div(className='header',	# Defining the hive_header so it can be called from the index.py file, class = 'header'
                       children= html.Div( # Defining the children for the header
                           className='header_children', # Class of children = 'header_children'
                           children=[	# Children inside of the header children, this is due to a right lay-out and styling
                                    html.Img(
                                        src = configuration_get("styling", "imagepath") + "branding/logo.png",
                                        className="logo" # The application logo at the left of the page, needs to be hosted on an external location
                                    ),
                                    html.Ul(className="links",	# Setting up a Ul Li menu containing multiple Li's, class = 'links'
                                            children=[
                                        html.Li(html.A('Start',
                                                       href="/pages/start",
                                                       className="header_link")
                                                ), # Li - class = 'header_link', links to a certain source
                                        html.Li(html.A('Search',
                                                       href="/pages/search",
                                                        className = "header_link")
                                                ), # Li - class = 'header_link', links to a certain source
                                        html.Li(html.A('Keyword search',
                                                       href="/pages/keywordsearch",
                                                        className = "header_link")
                                                ), # Li - class = 'header_link', links to a certain source
                                        html.Li(html.A('Settings',
                                                       href="/pages/settings",
                                                        className = "header_link")
                                                ) # Li - class = 'header_link', links to a certain source
                                    ])
                                ])
                        )
