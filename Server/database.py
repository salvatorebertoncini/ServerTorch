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

#Connect Mongo by means of creation of MongoClient
def connectMongoDB():
    return MongoClient(DBHOST, DBPORT)

#Close MongoClient connection
def closeMongoDB(client):
    client.close()

#Select the collection, implying dbname as default DBNAME
def selectCollectionMongoDB(client, dbname=DBNAME):
    db = client[dbname]
    return db[DBCOLLECTION]

#Select the latest N elements of a collection, returning them in a list
def selectLatestNElementsMongoDB(collection, N):
    return list(collection.find().skip(collection.count() - N))

#Insert and element into a collection
def insertElementMongoDB(collection, data):
    return collection.insert_one(data)
