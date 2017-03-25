#!/usr/bin/python

import MySQLdb

db = MySQLdb.connect("localhost","root","1","coding" )

cursor = db.cursor()

# Create table as per requirement
sql = """CREATE TABLE ACCOUNTS (
         username  CHAR(20) NOT NULL,
         password CHAR(20) )"""

cursor.execute(sql)

# Create table as per requirement
sql = """CREATE TABLE TASKS (serial int(11) NOT NULL AUTO_INCREMENT,
         id TEXT NOT NULL,
         username  CHAR(20) NOT NULL,
         urls TEXT NOT NULL,
         status CHAR NOT NULL,PRIMARY KEY(serial)) AUTO_INCREMENT=1 """

cursor.execute(sql)

# disconnect from server
db.close()
