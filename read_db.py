#!env/bin/python

import pymongo
from tables.basetable import DATABASE_NAME
from tables.playerstable import TABLE_NAME

connection = pymongo.Connection()
table = getattr(connection, DATABASE_NAME)[TABLE_NAME].find()

print "  The test database is named: '{}'".format(DATABASE_NAME)
print "  The records in the '{}' table are:".format(TABLE_NAME)

for record in table:
    max_len = max([len(k) for k in record.keys()])
    print " -------------------------------------------"
    for k in record.keys():
        print "     ", "{} :".format(k).rjust(max_len), record[k]
