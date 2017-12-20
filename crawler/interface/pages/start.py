#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_html_components as html
from utilities.config import *

layout = html.Div(style={'textAlign': 'center'},
                  children=[
                      html.Img(
                          src=configuration_get("styling", "imagepath") + "branding/favicon.png",
                          style={'width': 105,
                                 'marginLeft': 'auto',
                                 'marginRight': 'auto',
                                 'marginTop': 50}),
                      html.H2("Welcome at HIVE",
                              style={'maxWidth': 400,
                                     'marginLeft': 'auto',
                                     'marginRight': 'auto',
                                     'letterSpacing': '0.02em',
                                     'color': '#484848'}),

                      html.P("Version 2.0 - Prototype",
                             style={'fontSize': 14,
                                    'maxWidth': 400,
                                    'marginLeft': 'auto',
                                    'marginRight': 'auto',
                                    'fontWeight': 300,
                                    'marginTop': -20,
                                    'color': '#717171'}),

                      html.P('''HIVE is a Dark Web Crawler which crawles and scrapes the Dark Web 
                                and stores the content in an extremely fast database. Use the search 
                                page to search for information and content.''',
                             style={'maxWidth': 430,
                                    'marginLeft': 'auto',
                                    'marginRight': 'auto',
                                    'marginTop': 20,
                                    'color': '#555555'}),

                      html.P("The precondition to freedom is security.",
                             style={'marginLeft': 'auto',
                                    'marginRight': 'auto',
                                    'marginTop': 20,
                                    'fontStyle': 'italic'}),

                      html.A('User Guide',
                             href="/pages/userguide",
                             className="userguide_button"),

                      html.Div([
                          html.Div('''This application is created by FOUR. on behalf of the Hogeschool van Amsterdam. 
                          HIVE is a proof-of-concept self-managing Dark Web crawler which is able to scrape content 
                          and stores it in a database for later retrieval by analysts. This application is subject to 
                          the Open Source MIT-License which is available in the EULA. By using this application, 
                          you agree to the EULA. The operator of this application takes full responsibility when 
                          deploying this application. FOUR - 2017.''',
                                   className="barContent")
                      ], className="startBar")
])
