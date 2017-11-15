import dash_html_components as html

hive_header = html.Div(className='header',
                       children= html.Div(
                           className='header_children',
                           children=[
                                    html.Img(
                                        src="https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/Documents/HIVE/Images/HIVE.png?slrid=6714269e-8031-4000-938d-c9e3003f7c2c",
                                        className="logo"
                                    ),
                                    html.Ul(className="links",
                                            children=[
                                        html.Li(html.A('Start',
                                                       href="/pages/start")
                                                ),
                                        html.Li(html.A('Search',
                                                       href="/pages/search")
                                                ),
                                        html.Li(html.A('Keyword',
                                                       href="/pages/keywordsearch")
                                                ),
                                        html.Li(html.A('Settings',
                                                       href="/pages/settings")
                                                )
                                    ])
                                ])
                        )
