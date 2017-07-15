from mongoengine import *

DBNAME = 'ServerTorch'
DBHOST = 'localhost'
DBPORT = 27017
DBUSERNAME = ''
DBPASSWORD = ''

def connect():
    connect(DBNAME, host=DBHOST, port=DBPORT)

def close():
    connection.close()
