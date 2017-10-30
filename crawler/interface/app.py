import dash
app = dash.Dash()
app.css.append_css({'external_url': 'https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/_layouts/15/guestaccess.aspx?docid=10016fc7e13134c75a9bf4f10a403431c&authkey=AW1L7BrSmeLW2FvFqkixGsc'})
app.title = "HIVE - A Dark Web Crawler"
server = app.server
app.config.supress_callback_exceptions = True

