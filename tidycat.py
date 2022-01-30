# tidycat.py was designed to parse and sort the html data stored on
# raw-data_db.sqlite, and scrape those pages for an exploratory data
# analysis.

# Note: Windows has difficulty in displaying UTF-8 characters in the console so
# for each console window you open, you may need to type the following command
# before running this code :    chcp 65001

# Python Library imports :
from curses.ascii import FF
import sqlite3 as sqlite
import re
from bs4 import BeautifulSoup as GoodSoup

# Opens a connection for each database to be used, and limits the raw data to be read only.
raw_db = sqlite.connect('file:raw-data_db.sqlite?mode=ro', uri=True)
raw_sql = raw_db.cursor()
eda_db = sqlite.connect('eda-data_db.sqlite')
eda_sql = eda_db.cursor()

# Checks the database to ensure the correct tables exists, and generates them
# if they are missing. Also populates my fake boolean values because SQL doesn't
# support boolean logic for some reason?
eda_sql.execute('CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY, company TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS brands (id INTEGER PRIMARY KEY, brand TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS flavours (id INTEGER PRIMARY KEY, flavour TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY, company TEXT UNIQUE)')
# Creating a table that will fake boolean logic for me.
eda_sql.execute('CREATE TABLE IF NOT EXISTS analysis_type(id BIT PRIMARY KEY, type TEXT UNIQUE)')
eda_sql.execute('INSERT OR IGNORE INTO analysis_type (type) VALUES (?)', ('ga'))
eda_sql.execute('INSERT OR IGNORE INTO analysis_type (type) VALUES (?)', ('ta'))
# As above, faking that boolean logic.
eda_sql.execute('CREATE TABLE IF NOT EXISTS valcalc_type (id BIT PRIMARY KEY, type TEXT UNIQUE)')
eda_sql.execute('INSERT OR IGNORE INTO valcalc_type (type) VALUES (?)', ('dmb'))
eda_sql.execute('INSERT OR IGNORE INTO valcalc_type (type) VALUES (?)', ('wmb'))
# The composite table for each can_value entry.
eda_sql.execute('''CREATE TABLE IF NOT EXISTS can_values (id INTERGER PRIMARY KEY, company_id INTERGER, brand_id INTERGER, 
flavour_id INTERGER, analysis_id INTERGER, valcalc_id INTERGER, )
''')

# Building tidycat specific functions.


# Pulling in HTML code from raw-data_db.sqlite for sorting.
raw_sql.execute('SELECT parsetext FROM page_list')
row = raw_sql.fetchone()
for htmltags in row[2] :
### DEBUGGING ###
    print(htmltags)