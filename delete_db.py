#!env/bin/python
import pymongo
from tables.basetable import DATABASE_NAME

connection = pymongo.Connection()
connection.drop_database(DATABASE_NAME)
