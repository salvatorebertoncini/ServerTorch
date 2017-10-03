from pymongo import MongoClient
import json

"""
per collegarsi al db:

exec su kinect
mongo
use SpyTorch
db.aggregate.find() per vedere tutto
"""

DBNAME = 'SpyTorch'
DBFETCHNAME = 'datafetching'
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
def selectLatestNElementsMongoDB(N):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    if N == 0:
        return list(collection.find())
    else:
        return list(collection.find().skip(collection.count() - N))


def selectAllUsers():
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.find()


# Select user with slug
def selectUserWithSlug(slug):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.find({"UserInfo": {"Username": slug}})


def selectDevicesWithSlug(slug):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.find({"TelephoneInfo.IMEI": slug})


def selectMessagesList(username):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.find({"MessageUsername": username})


def insertMessageList(message):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.insert_one(message)


def updateMessageList(username, message):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.update({"MessageUsername": username}, message)

#Insert and element into a collection
def insertElementMongoDB(data):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)
    closeMongoDB(client)

    return collection.insert_one(data)

def initializeDB():
    #Initialize client
    client = connectMongoDB()

    #select datafetch collection
    collection = selectCollectionMongoDB(client, DBFETCHNAME)

    #Check if storing DB is empty
    if collection.count() == 0:
        data = { "date": "", "stats": {"BuildInfo": {"Manufacturers": {"devices":[],"totalCounter": 0 } },"flag": True }}
        insertElementMongoDB(collection, data)

    #close mongo client
    closeMongoDB(client)
