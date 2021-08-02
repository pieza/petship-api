import os
from pymongo import MongoClient

conn_string = os.environ['DB_CONN']
db = MongoClient(conn_string)['petship']
