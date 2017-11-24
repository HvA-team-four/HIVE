import dash_html_components as html

layout = html.Div([
    html.H3('Settings'),
    html.P("Use this page to view and navigate to the settings of HIVE. Please select a tile to navigate to the desired settings category.", style={"width":400}),
    html.Br(),
    html.Div([
    html.A([
        html.Img(
                src="https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/_layouts/15/guestaccess.aspx?docid=031401fe19ac44729a19f9365d9e3b8f2&authkey=AcDrC_XFIBy4mHjiA-wVD9M&e=e3935862cbd54b5c9cbdf4f4112f3a66",
                className="settingIcon"
                                    ),
        html.P("URL", className='settingTitle')


    ], href="urlsettings", className='setting'),

    html.A([
        html.Img(
                src="https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/_layouts/15/guestaccess.aspx?docid=13156e54bd4ff47479b21803dea30991e&authkey=AddQVpwAP46MQBcfaNXDyQw&e=87f544e7861149c684a3439e60cecc82",
                className="settingIcon"
                                    ),
        html.P("Keyword", className='settingTitle')
    ], href="keywordsettings", className='setting'),

    html.A([
            html.Img(
                    src="https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/_layouts/15/guestaccess.aspx?docid=13156e54bd4ff47479b21803dea30991e&authkey=AddQVpwAP46MQBcfaNXDyQw&e=87f544e7861149c684a3439e60cecc82",
                    className="settingIcon"
                                        ),
            html.P("User Guide", className='settingTitle')
        ], href="userguide", className='setting'),

    ], className = 'hivesettings')
])
