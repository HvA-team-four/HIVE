#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_html_components as html
from utilities.config import *

# Defining the lay-out of this page.
layout = html.Div([
    html.H3('Settings'),

    html.P('''Use this page to view and navigate to the settings of HIVE.
           Please select a tile to navigate to the desired settings category.''',
           style={"width": 400}),

    html.Br(),

    html.Div([
        # Each of these html.A() tags display a settings box (URL, Keyword, User Guide, etc.)
        html.A([
            html.Img(
                    src=configuration_get("styling", "imagepath") + "settings/url.png",
                    className="settingIcon"),
            html.P("URL", className='settingTitle')
        ], href="urlsettings", className='setting'),

        html.A([
            html.Img(
                    src=configuration_get("styling", "imagepath") + "settings/keyword.png",
                    className="settingIcon"),
            html.P("Keyword", className='settingTitle')
        ], href="keywordsettings", className='setting'),

        html.A([
            html.Img(
                src=configuration_get("styling", "imagepath") + "settings/contentblock.png",
                className="settingIcon"),
            html.P("Content Block", className='settingTitle')
        ], href="blocksettings", className='setting'),

        html.A([
            html.Img(
                src=configuration_get("styling", "imagepath") + "settings/configuration.png",
                className="settingIcon"),
            html.P("Configuration", className='settingTitle')
        ], href="configurationsettings", className='setting'),

        html.A([
            html.Img(
                src=configuration_get("styling", "imagepath") + "settings/userguide.png",
                className="settingIcon"),
            html.P("User Guide", className='settingTitle')
        ], href="userguide", className='setting'),

        html.A([
            html.Img(
                src=configuration_get("styling", "imagepath") + "settings/searchlog.png",
                className="settingIcon"),
            html.P("Search Log", className='settingTitle')
        ], href="searchlog", className='setting'),



    ], className='hivesettings')
])
