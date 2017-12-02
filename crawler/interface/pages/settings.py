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
            src="https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/_layouts/15/guestaccess.aspx?docid=148670e21e5e34731a76800955afbe657&authkey=AURSMDKWsa1tf8A-b80ehXU&e=ab3935accbb24c7589dc0c1c32b75026",
            className="settingIcon"
        ),
        html.P("Content Block", className='settingTitle')
    ], href="blocksettings", className='setting'),


    html.A([
            html.Img(
                    src="https://herke-my.sharepoint.com/:i:/g/personal/t_lambalk_herke_nl/EUxGjY93y4NNsBLytHZ6048B5NKq_YXJzDbdzrlqF3NJJw?e=d512d69044ec4739bc37dc911abdacee",
                    className="settingIcon"
                                        ),
            html.P("Configuration", className='settingTitle')
        ], href="configurationsettings", className='setting'),

    html.A([
        html.Img(
            src="https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/_layouts/15/guestaccess.aspx?docid=170ca763ad91b483ea269444f1a401607&authkey=ASirnpM17tNbnL0v25GpuJ8&e=9b46697960644b40b4fb53f2f60b3926",
            className="settingIcon"
        ),
        html.P("User Guide", className='settingTitle')
    ], href="userguide", className='setting'),

    ], className = 'hivesettings')
])


