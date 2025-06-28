'''
Настройки подключения к базам данных MySQL и MongoDB
для проекта final_project.
'''

import pymongo
import pymysql

DATABASE_MYSQL_W = {
    'host': 'ich-db.edu.itcareerhub.de',
    'user': 'ich1',
    'password': 'password',
    'database': 'sakila',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

DATABASE_MYSQL_NAME = 'sakila'

MONGO_CLIENT = pymongo.MongoClient(
    'mongodb://ich_editor:verystrongpassword'
    '@mongo.itcareerhub.de/?readPreference=primary'
    '&ssl=false&authMechanism=DEFAULT&authSource=ich_edit'
)

DATABASE_MONGO = MONGO_CLIENT['ich_edit']
MY_COLLECTION_MONGO = DATABASE_MONGO['final_project_100125_Kseniia']
