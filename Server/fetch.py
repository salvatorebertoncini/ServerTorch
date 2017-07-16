import datetime

from database import *


def fetchData(data):

    client = connectMongoDB()
    collection = selectCollectionMongoDB(client, "datafetching")

    #select latest element
    latest = selectLatestNElementsMongoDB(collection, 1)

    #fetch element example
    counter = latest[0]["counter"]
    date = latest[0]["date"]
    inndate = latest[0]["map"]["date"]
    print "date latest element: "+str(date)+"\n"
    print "innested date element: "+str(inndate)+"\n"

    #insert new results
    latest = {"date": datetime.datetime.now(), "map" : data, "counter": counter+1}

    #save fetched element
    result = insertElementMongoDB(collection, latest)
    print 'Successfully inserted, with ID: {0}'.format(result.inserted_id)

    closeMongoDB(client)
