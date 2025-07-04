'''
Module for database connection settings and connection helpers
for MySQL and MongoDB.
'''

import os
from dotenv import load_dotenv
from pymysql.err import MySQLError
from pymongo.errors import PyMongoError
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


def create_mysql_connection():
    '''
    Creates and returns a universal connection to MySQL.
    Suitable for both reading and writing if you use a user with proper privileges.
    '''

    try:
        connection_query = pymysql.connect(**DATABASE_MYSQL_W)
        return connection_query
    except MySQLError as e:
        raise MySQLError(f'Error connecting to MySQL: {e}') from e


def get_mongo_collection():
    '''
    Returns a connection to the fixed MongoDB collection.
    '''

    try:
        return MY_COLLECTION_MONGO
    except PyMongoError as e:
        raise PyMongoError(f'Error connecting to MongoDB Collection: {e}') from e
