import datetime

from database import *
from logs import saveLog

def fetchData(data):

    #MongoDB connection, selecting "datafetching" database
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client, "datafetching")

    #Select latest element
    latest = selectLatestNElementsMongoDB(collection, 1)

    #Fetch element example
    counter = latest[0]["counter"]
    date = latest[0]["date"]
    inndate = latest[0]["map"]["date"]
    print "\ndate latest element: "+str(date)
    print "innested date element: "+str(inndate)+"\n"

    #Insert new results
    latest = {"date": datetime.datetime.now(), "map" : data, "counter": counter+1}

    #Save fetched element
    result = insertElementMongoDB(collection, latest)
    saveLog('fetch.py','Successfully inserted with ID: {0}'.format(result.inserted_id)+'\n')

    #Closing connection
    closeMongoDB(client)
