from pymongo import MongoClient

DBNAME = 'SpyTorch'
DBHOST = 'localhost'
DBPORT = 27017
DBUSERNAME = ''
DBPASSWORD = ''

def connectMongoDB():
    return MongoClient(DBHOST, DBPORT)

def closeMongoDB(self):
    self.close()
