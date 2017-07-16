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


def selectCollectionMongoDB(client, dbname=DBNAME):
    db = client[dbname]
    return db[DBCOLLECTION]


def selectLatestNElementsMongoDB(collection, N):
    return list(collection.find().skip(collection.count() - N))


def insertElementMongoDB(collection, data):
    return collection.insert_one(data)
