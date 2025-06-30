import os
from dotenv import load_dotenv
import pymysql
import pymongo

load_dotenv()

print("MONGO_DB =", os.getenv('MONGO_DB'))
print("MONGO_URI =", os.getenv('MONGO_URI'))

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