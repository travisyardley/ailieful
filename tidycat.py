# tidycat.py was designed to parse and sort the html data stored on
# raw-data_db.sqlite, and scrape those pages for an exploratory data
# analysis.

# Note: Windows has difficulty in displaying UTF-8 characters in the console so
# for each console window you open, you may need to type the following command
# before running this code :    chcp 65001

# Python Library imports :
import sqlite3 as sqlite

# Establishes connection to SQL server and an associated cursor method.
eda_db = sqlite.connect('eda-data_db.sqlite')
eda_sql = eda_db.cursor()

# Checks the database to ensure the correct tables exists, and generates them
# if they are missing. Also populates my fake boolean values because SQL doesn't
# support boolean logic for some reason?
eda_sql.execute('CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY, company TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS brands (id INTEGER PRIMARY KEY, brand TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS flavours (id INTEGER PRIMARY KEY, flavour TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY, company TEXT UNIQUE)')
eda_sql.execute('CREATE TABLE IF NOT EXISTS analysis_type(id BIT PRIMARY KEY, type TEXT UNIQUE)')
eda_sql.execute('INSERT OR IGNORE INTO analysis_type (type) VALUES (?)', ('ga'))
eda_sql.execute('INSERT OR IGNORE INTO analysis_type (type) VALUES (?)', ('ta'))
eda_sql.execute('CREATE TABLE IF NOT EXISTS valcalc_type(id BIT PRIMARY KEY, type TEXT UNIQUE)')
eda_sql.execute('INSERT OR IGNORE INTO valcalc_type (type) VALUES (?)', ('dmb'))
eda_sql.execute('INSERT OR IGNORE INTO valcalc_type (type) VALUES (?)', ('wmb'))