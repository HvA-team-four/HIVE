import dash

app = dash.Dash()
app.title = "HIVE - A Dark Web Crawler"
server = app.server
app.config.supress_callback_exceptions = True

my_css_url = "https://raw.githubusercontent.com/HvA-team-four/HIVE/DashInterface/crawler/interface/assets/hive.css"
app.css.append_css({
    "external_url": my_css_url
})