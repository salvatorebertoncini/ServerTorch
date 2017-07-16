import datetime

from database import *
from logs import saveLog

#JSON Example
#{ "date": "", "stats": {"BuildInfo": {"Manufacturer": [], "ManufacturerCounter": 0 }, "TelephoneInfo":  { "IMEIcounter": 0, "IMEIcollected": []} },"flag": true }


def IMEIFetch(imei, imeiList, imeiCounter):
    if imei not in imeiList:
        imeiCounter += 1
        imeiList.append(imei)
    return imeiList, imeiCounter


def ManufacturerFetch(device, deviceList, deviceCounter):
    if device not in deviceList:
        deviceList.append(device)
        deviceCounter += 1
    return deviceList, deviceCounter


def DevicePercentage(device, deviceList, deviceCounter):
    if device in deviceList:
        return 1 / deviceCounter
    else:
        return 0


def fetchData(data):
    #MongoDB connection, selecting "datafetching" database
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client, "datafetching")

    #Select latest element
    latest = selectLatestNElementsMongoDB(collection, 1)

    #Fetch IMEI
    imeiList = latest[0]["stats"]["TelephoneInfo"]["IMEIcollected"]
    imeiCounter = latest[0]["stats"]["TelephoneInfo"]["IMEIcounter"]
    imeiList, imeiCounter = IMEIFetch(data["TelephoneInfo"]["IMEI"], imeiList, imeiCounter)


    #Fetch Manufacturer
    deviceList = latest[0]["stats"]["BuildInfo"]["Manufacturer"]
    deviceCounter = latest[0]["stats"]["BuildInfo"]["ManufacturerCounter"]
    deviceList, deviceCounter = ManufacturerFetch(data["BuildInfo"]["Manufacturer"], deviceList, deviceCounter)

    #e.g. percentage of Samsung devices in the database
    samsung = DevicePercentage("Samsung", deviceList, deviceCounter)

    #e.g. percentage of Apple devices in the database, LOL
    apple = DevicePercentage("Apple Inc.", deviceList, deviceCounter)

    """   
    #LambdaFetch with map function
    lambdaf = map(lambda x: x["counter"]+1000, latest)
    print "lambda function -> "+str(lambdaf)
    """

    #Insert new results
    latest = { "date": datetime.datetime.now(), "stats": {"BuildInfo": {"Manufacturer": deviceList, "ManufacturerCounter": deviceCounter }, "TelephoneInfo":  {"IMEIcounter": imeiCounter, "IMEIcollected": imeiList} },"flag": True }

    #Save fetched element
    result = insertElementMongoDB(collection, latest)
    saveLog('fetch.py','Successfully inserted with ID: {0}'.format(result.inserted_id)+'\n')
    saveLog('fetch.py', "Percentuale dispositivi Samsung: %s" % str(samsung))
    saveLog('fetch.py', "Percentuale dispositivi Apple: %s" % str(apple))

    #Closing connection
    closeMongoDB(client)
