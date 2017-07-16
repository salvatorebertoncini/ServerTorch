from pymongo import MongoClient

"""
per collegarsi al db:

exec su kinect
mongo
use SpyTorch
db.aggregate.find() per vedere tutto
"""

DBNAME = 'SpyTorch'
DBCOLLECTION = 'aggregate'
DBHOST = 'localhost'
DBPORT = 32768
DBUSERNAME = ''
DBPASSWORD = ''


def connectMongoDB():
    return MongoClient(DBHOST, DBPORT)


def closeMongoDB(client):
    client.close()


def selectCollectionMongoDB(client):
    db = client[DBNAME]
    return db[DBCOLLECTION]

def selectCollectionMongoDB(client, collection):
    db = client[DBNAME]
    return db[collection]


def selectElementMongoDB(client):
    return 1


def insertElementMongoDB(collection, data):
    return collection.insert_one(data)
