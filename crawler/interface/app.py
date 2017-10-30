import dash

app = dash.Dash()
app.css.append_css({'external_url': 'https://herke-my.sharepoint.com/personal/t_lambalk_herke_nl/_layouts/15/guestaccess.aspx?docid=1a328c2860b4b4e66b806b1b92ff5a8b2&authkey=ASrYUvcKKW1vlc60Pe1O3Cc'})
app.title = "HIVE - A Dark Web Crawler"
server = app.server
app.config.supress_callback_exceptions = True

