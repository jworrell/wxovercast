'''
Created on May 24, 2013

@author: jworrell

REQUIRES DATA FROM: http://www.ourairports.com/data/
'''

import csv
import sqlite3

CSV_LOCATION = "/Users/jworrell/Desktop/airports.csv"
DATA_LOCATION = "/Users/jworrell/Desktop/airports.db"

INSERT_SQL = "INSERT INTO airports VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

def main():
    with open(CSV_LOCATION) as airports_file:
        with sqlite3.connect(DATA_LOCATION) as airports_conn:
            airports_conn.text_factory = str
            
            airports_reader = csv.reader(airports_file)
            airports_conn.executemany(INSERT_SQL, airports_reader)

            airports_conn.commit()

if __name__ == '__main__':
    main()