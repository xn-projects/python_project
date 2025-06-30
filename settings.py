import os
from dotenv import load_dotenv
import pymysql
import pymongo

load_dotenv()

DATABASE_MYSQL_W = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'charset': os.getenv('MYSQL_CHARSET'),
    'cursorclass': pymysql.cursors.DictCursor
}

DATABASE_MYSQL_NAME = os.getenv('MYSQL_DATABASE')

MONGO_CLIENT = pymongo.MongoClient(os.getenv('MONGO_URI'))

DATABASE_MONGO = MONGO_CLIENT[os.getenv('MONGO_DB')]
MY_COLLECTION_MONGO = DATABASE_MONGO[os.getenv('MONGO_COLLECTION')]

COLORS = {
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "red": "\033[91m",
    "green": "\033[92m",
    "reset": "\033[0m"
}