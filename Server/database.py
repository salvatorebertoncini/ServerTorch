from pymongo import MongoClient

"""
per collegarsi al db:

exec su kinect
mongo
use SpyTorch
db.aggregate.find() per vedere tutto
"""

DBNAME = 'SpyTorch'
DBHOST = 'localhost'
DBPORT = 32768
DBUSERNAME = ''
DBPASSWORD = ''

def connectMongoDB():
    return MongoClient(DBHOST, DBPORT)

def closeMongoDB(client):
    client.close()
