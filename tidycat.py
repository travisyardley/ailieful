# tidycat.py was designed to parse and sort the html data stored on
# raw-data_db.sqlite, and scrape those pages for an exploratory data
# analysis.

# Note: Windows has difficulty in displaying UTF-8 characters in the console so
# for each console window you open, you may need to type the following command
# before running this code :    chcp 65001

# Python Library imports :
import sqlite3 as sqlite
import re

# Opens a connection for each database to be used, and limits the raw data to be read only.
raw_db = sqlite.connect('file:raw-data_db.sqlite?mode=ro', uri=True)
raw_sql = raw_db.cursor()
eda_db = sqlite.connect('eda-data_db.sqlite')
eda_sql = eda_db.cursor()

# Checks the database to ensure the correct tables exists, and generates them
# if they are missing. Also populates my fake boolean values because SQL doesn't
# support boolean logic for some reason?
eda_sql.execute('CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS brands (id INTEGER PRIMARY KEY AUTOINCREMENT, brand TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS flavours (id INTEGER PRIMARY KEY AUTOINCREMENT, flavour TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS analysis_type(bool BIT PRIMARY KEY, type TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS valcalc_type (bool BIT PRIMARY KEY, type TEXT UNIQUE)')

# The composite table for each can_value entry.
eda_sql.execute('''CREATE TABLE IF NOT EXISTS can_values (id INTERGER PRIMARY KEY, company_id INTERGER, brand_id INTERGER, 
flavour_id INTERGER, analysis_id INTERGER, valcalc_id INTERGER)
''')
eda_db.commit()

# Populating tables for my fake boolean.
eda_sql.execute('INSERT OR IGNORE INTO analysis_type (bool,type) VALUES (?,?)', (0,'ga'))
eda_sql.execute('INSERT OR IGNORE INTO analysis_type (bool,type) VALUES (?,?)', (1,'ta'))
eda_sql.execute('INSERT OR IGNORE INTO valcalc_type (bool,type) VALUES (?,?)', (0,'dmb'))
eda_sql.execute('INSERT OR IGNORE INTO valcalc_type (bool,type) VALUES (?,?)', (1,'wmb'))
eda_db.commit()

# Building tidycat specific functions.

# Pulling in HTML code from raw-data_db.sqlite for sorting.
raw_sql.execute('SELECT parsetext FROM page_list')
row = raw_sql.fetchone()
for htmltags in row :
### DEBUGGING ###
    print(htmltags)