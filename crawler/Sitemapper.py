from bs4 import BeautifulSoup
import pymysql
import requests
import time

# Open database connection
db = pymysql.connect("localhost","root","password","naomi")

# prepare a cursor object using cursor() method
cursor = db.cursor()

#now crawl the url
url = "https://www.google.com"

r  = requests.get(url)

data = r.text

soup = BeautifulSoup(data, "html5lib")
urlArray = []

for link in soup.find_all('a'):
    urlArray.append(link.get('href')) #add to array

for x in range(len(urlArray)): 
    if urlArray[x].startswith('/'): #when the array element string starts with '\'
        urlArray[x] = url + urlArray[x]
          
for i in range(len(urlArray)):
    print(urlArray[i])
    
    date = time.strftime("%c")

    print (date)

# Prepare SQL query to INSERT a record into the database.
    sql = """INSERT INTO sitemapper(url, date)
    VALUES (%s, '%s')"""

# execute SQL query using execute() method.
    cursor.execute(sql, (urlArray[i], date))

    db.commit()

# disconnect from server
db.close()

