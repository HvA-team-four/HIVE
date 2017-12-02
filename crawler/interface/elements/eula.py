import dash_html_components as html # Importing Dash HTML components as html
import dash_core_components as dcc

hive_termsofuse = html.Div(
    html.Div([
    html.H3("End-User License Agreement"),
    html.Div([
        dcc.Markdown('''
###### Article 1 - Licensing (MIT)
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

###### Article 2 - Authors
1.1 This application is created by **FOUR.** on behalf of the Hogeschool van Amsterdam 
during the project in the security semester. This application is created in close 
cooperation with Deloitte.

1.2 This application is created as a proof of concept and is not tested nor certified 
for use in a operational environment. This application is licensed under the MIT 
license, which is available in article 2.  

###### Article 3 - Service and maintenance
3.1 The organisation using this application is responsible for maintaining the code. **FOUR. will not be hold responsible for any interruptions during running the application and FOUR. will not be available for service-requests. 

3.2 This application comes without warranty or service. **FOUR.** cannot be hold responsible for malfunction of the application and any effects of malfunction. 

###### Article 4 - Effects
4.1 Using this application can cause websites to block the IP-address of the organization using the application. 

###### Article 5 - Data an illegal content
5.1 **FOUR.** is not responsible for any data, legal or illegal, that is scraped/retrieved by the crawler and stored in the database. 

5.2 The application makes NO use of a VPN connection to connect to the dark web, a TOR proxy is used to crawl the dark web. 

5.3 The application stores all content/data from the websites it crawles in the database. By default, the application does not block any illegal content and the interface does not provide a way to delete illegal content from the database. Neither **FOUR.** or the Hogeschool van Amsterdam are responsible for the possibility of illegal content being stored.

###### Article 6 - Usage and searches
6.1 The application provides an interface which enables users to search the database for content. The application does not automatically block searches for illegal content, neither **FOUR.** or the Hogeschool van Amsterdam are responsible for (illegal) searches done by users of the application. 
'''
)], className="termsText"),

html.Button('Close', id='closeTerms')


], className = "termsOfUseBox"
), className="termsOfUseBackground"
)

hive_bottombar = html.Div([
    "By using this application, you agree to the",
    html.Button('License Agreement', className="openTermsButton", id="TermsButton")
]
    ,className = "termsOfUseBar", id="termsOfUseBar"
)