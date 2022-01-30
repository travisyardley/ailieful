# sypdercat.py was designed to crawl through a predefined array of websites,
# record html on raw-data_db.sqlite, and scrape those pages for an exploratory
# data analysis.

# Note: Windows has difficulty in displaying UTF-8 characters in the console so
# for each console window you open, you may need to type the following command
# before running this code :    chcp 65001

# Python Library imports :
import sqlite3 as sqlite
import ssl
import requests
import random
from bs4 import BeautifulSoup as GoodSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import urllib.request

# Ignores SSL certificate errors :
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# D-d-don't be suspicious, don't be suspicious...
# Don't be suspicious, ah! Don't be suspicious...
# Header info for the User Agent randomizer I ended up needing,
# because cat food is serious business.
agent_headers = [
# Firefox 77 Mac
{
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Referer': 'https://www.google.com/',
'DNT': '1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1'
},
# Firefox 77 Windows
{
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://www.google.com/',
'DNT': '1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1'
},
# Chrome 83 Mac
{
'Connection': 'keep-alive',
'DNT': '1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Dest': 'document',
'Referer': 'https://www.google.com/',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
},
# Chrome 83 Windows 
{
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-User': '?1',
'Sec-Fetch-Dest': 'document',
'Referer': 'https://www.google.com/',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9'
}
]

# DON'T BE SUSPICIOUS!
# Building a dictionary for the User Agent randomizer, because again: cat food. 
agent_list = []
for headers in agent_headers:
    h = dict()
for header,value in headers.items() :
    h[header]=value
    agent_list.append(h)
url = 'https://httpbin.org/headers'

# Randomizes agent selection.
for i in range(1,4):
    headers = random.choice(agent_headers)

# Creates a request session.
req = requests.Session()
req.headers = headers
secretagent = req.get(url)

# That should take care of the secret agent stuff.

# Establishes connection to SQL server and an associated cursor method.
raw_db = sqlite.connect('raw-data_db.sqlite')
raw_sql = raw_db.cursor()

# Checks the database to ensure the correct tables exists, and generates them
# if they are missing.
raw_sql.execute('CREATE TABLE IF NOT EXISTS crawl_list (url TEXT UNIQUE)')
raw_sql.execute('CREATE TABLE IF NOT EXISTS page_list (id INTEGER PRIMARY KEY, url TEXT UNIQUE, parsetext TEXT, errorcode INTEGER)')

# Defines the websites to be crawled.
crawl_list = ['http://webcache.googleusercontent.com/search?q=cache:https://catfooddb.com/']

# Checks progress of current spidering efforts, and either resumes or resets
# based on conditions.
raw_sql.execute('SELECT id,url FROM page_list WHERE parsetext is NULL and errorcode is NULL ORDER BY RANDOM() LIMIT 1')
row = raw_sql.fetchone()
if row is not None :
    print('Restarting existing crawl. Deleting raw-data_db.sqlite will reset the crawl.')
else :
    print('Enter a URL to add to the crawl list, or press enter to run the crawl_list as is.')
    starturl = input(' ')
    if len(starturl) < 1 :
        starturl = random.choice(crawl_list)
    if ( starturl.endswith('/') ) : 
        starturl = starturl[:-1]
    if ( starturl.endswith('.htm') or starturl.endswith('.html') ) :
        pos = starturl.rfind('/')
        starturl = starturl[:pos]
    weburl = starturl
    if ( len(weburl) > 1 ) :
        raw_sql.execute('INSERT OR IGNORE INTO crawl_list (url) VALUES (?)', (weburl,))
        raw_sql.execute('INSERT OR IGNORE INTO page_list (url, parsetext) VALUES (?, NULL)', (starturl,))
        raw_db.commit()

# Get the current website from crawl_list
raw_sql.execute('SELECT url FROM crawl_list')
weblist = list()
for row in raw_sql:
    weblist.append(str(row[0:]))
print(weblist)
itcounter = 0
while True:
    if ( itcounter < 1 ) :
        print('Enter the number of pages to retrieve, or press ENTER to break.')
        sval = input(' ')
        if ( len(sval) < 1 ) :
            break
        itcounter = int(sval)
    itcounter = itcounter - 1
    raw_sql.execute('SELECT id,url FROM page_list WHERE parsetext is NULL and errorcode is NULL ORDER BY RANDOM() LIMIT 1')
    try:
        row = raw_sql.fetchone()
### DEBUGGING ###
        #print(row)
        fromid = row[0]
        url = row[1]
    except:
        print('-------------------')
        print('No unretrieved HTML pages found. Closing the spidercat.')
        itcounter = 0
        break
    print(fromid, url, end=' ')

# Generates the secret User-Agent to used for the request.
    try:     
        request = urllib.request.Request(url, headers = secretagent, context=ctx)
        with urllib.request.urlopen(request) as response :
            html = response.read()
        print('-------------------')
        print('Secret User-Agent has been sent!\n%s'%(headers['User-Agent']))
        print('This is your secret (user) agent for the current crawl.')
        print('-------------------')
### DEBUGGING ###
        #print('Recevied by HTTPBin:')
        #print(secretagent.json())
        #print('-------------------')

# Checks for inaccessable pages, or pages that do not contain 
# any text or HTML to parse.
        if html.getcode() != 200 :
            print('Error flagged: ',html.getcode())
            raw_sql.execute('UPDATE page_list SET errorcode=? WHERE url=?', (html.getcode(), url))
        if 'text/html' != html.info().get_content_type() :
            print('This page did no contain text or html to parse.')
            raw_sql.execute('DELETE FROM page_list WHERE url=?', (url,))
            raw_db.commit()
            continue
        print('('+str(len(html))+')', end=' ')
        soup = GoodSoup(html, 'html.parser')
    except KeyboardInterrupt :
        print('-------------------')
        print('Program manually stopped.')
        break
    except:
        print('\n-------------------')
        print('Unable to retrieve or parse page.\nSomething went wrong in the request.urlopen TRY block.')
        raw_sql.execute('UPDATE page_list SET errorcode=-1 WHERE url=?', (url, ) )
        raw_db.commit()
        continue
    raw_sql.execute('INSERT OR IGNORE INTO page_list (url, parsetext) VALUES ( ?, NULL)', (url,))
    raw_sql.execute('UPDATE page_list SET parsetext=? WHERE url=?', (memoryview(html), url ))
    raw_db.commit()

# Searching for additional links on the page; checking for inaccessable suffixes,
# relative references, or tricky CSS honeypotting nonsense.
    pagetags = soup('')
    counter = 0
    for tag in pagetags:
        href = tag.get('href', None)
        if ( href is None ) :
            continue
        up = urlparse(href)
        if ( len(up.scheme) < 1 ) :
            href = urljoin(url, href)
        ipos = href.find('#')
        if ( ipos > 1 ) :
            href = href[:ipos]
        if ( href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') or href.endswith('.pdf') ) :
            continue
        if ( href.endswith('/') ) :
            href = href[:-1]
        if ( len(href) < 1 ) :
            continue

# References the current url against the crawl_list.
        found = False
        for web in weblist:
            if ( href.startswith(web) ) :
                found = True
                break
        if not found :
            continue
        raw_sql.execute('INSERT OR IGNORE INTO page_list (url, parsetext) VALUES (?, ?)', ( href, html))
        counter = counter + 1
        raw_db.commit()
        raw_sql.execute('SELECT id FROM page_list WHERE url=? LIMIT 1', ( href,))
        try :
            row = raw_sql.fetchone()
            toid = row[0]
        except :
            print('Could not retrieve id')
            continue
    print(counter)
raw_sql.close()
