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
    imeiList = latest[0]["stats"]["TelephoneInfo"]["IMEIcollected"]

    #if IMEI is not in db list
    if data["TelephoneInfo"]["IMEI"] not in imeiList :
        imeiCounter = latest[0]["stats"]["TelephoneInfo"]["IMEIcounter"]
        imeiCounter += 1
        imeiList.append(data["TelephoneInfo"]["IMEI"])

    #if Manufacturer is not in db list
    deviceList = latest[0]["stats"]["BuildInfo"]["Manufacturer"]
    if data["BuildInfo"]["Manufacturer"] not in deviceList:
        deviceList.append(data["BuildInfo"]["Manufacturer"])
        deviceCounter = latest[0]["stats"]["BuildInfo"]["ManufacturerCounter"]
        deviceCounter += 1

    #e.g. percentage of Samsung devices in the database
    if "Samsung" in deviceList:
        samsung = 1 / deviceCounter

    """   
    #LambdaFetch with map function
    lambdaf = map(lambda x: x["counter"]+1000, latest)
    print "lambda function -> "+str(lambdaf)
    """

    #Insert new results
    latest = { "date": datetime.datetime.now(), "stats": {"BuildInfo": {"Manufacturer": deviceList, "ManufacturerCounter": deviceCounter }, "TelephoneInfo":  {"IMEIcounter": imeiCounter, "IMEIcollected": imeiList} },"flag": True }

    #Save fetched element
    result = insertElementMongoDB(collection, latest)
    saveLog('fetch.py','Successfully inserted with ID: {0}'.format(result.inserted_id)+'\n'+ "Percentuale dispositivi Samsung: %s" % str(samsung))

    #Closing connection
    closeMongoDB(client)
