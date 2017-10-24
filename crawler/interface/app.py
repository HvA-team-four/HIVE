import dash

app = dash.Dash()
app.title = "HIVE - A Dark Web Crawler"
server = app.server
app.config.supress_callback_exceptions = True
app.css.config.serve_locally = True
