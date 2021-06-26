import sqlite3
import os
con = sqlite3.connect("C:\\Users\\Biplob\\OneDrive\\Desktop\\twitter\\TwitterSentiment\\src\\twitter.db")
cur = con.cursor()

for row in cur.execute("SELECT * FROM sentiment"):
    print(row)