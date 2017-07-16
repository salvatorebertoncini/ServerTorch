import datetime

from database import *
from logs import saveLog

#JSON Example
#{ "date": "", "stats": {"BuildInfo": {"Manufacturer": [], "ManufacturerCounter": 0 }, "TelephoneInfo":  { "IMEIcounter": 0, "IMEIcollected": []} },"flag": true }


def ManufacturerFetch(device, imei, deviceList):

    dev = filter(lambda x: x["Brand"] == device, deviceList["device"])
    print dev

    if not dev:
        counter = 1
        deviceList["device"].append({"IMEI": [imei], "Brand": device, "counter": counter})
    else:
        map(lambda x: [x["IMEI"].append(imei), x["counter"] + 1], filter(lambda x: x["Brand"] == device, deviceList["device"]))

    #deviceList["totalCounter"] += 1

    return deviceList


def DevicePercentage(device, deviceList):
    if device in deviceList.keys():
        return deviceList[device] / len(deviceList)
    else:
        return 0


def fetchData(data):
    #MongoDB connection, selecting "datafetching" database
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client, "datafetching")

    #Select latest element
    latest = selectLatestNElementsMongoDB(collection, 1)

    #Fetch Manufacturer
    BuildInfoList = latest[0]["stats"]["BuildInfo"]["Manufacturer"]
    BuildInfoList = ManufacturerFetch(data["BuildInfo"]["Manufacturer"], data["TelephoneInfo"]["IMEI"], BuildInfoList)

    #e.g. percentage of Samsung devices in the database
    samsung = DevicePercentage("Samsung", BuildInfoList)

    #e.g. percentage of Apple devices in the database, LOL
    apple = DevicePercentage("Apple Inc.", BuildInfoList)

    """   
    #LambdaFetch with map function
    lambdaf = map(lambda x: x["counter"]+1000, latest)
    print "lambda function -> "+str(lambdaf)
    """

    #Insert new results
    latest = { "date": datetime.datetime.now(), "stats": {"BuildInfo": {"Manufacturer": BuildInfoList}},"flag": True }

    #Save fetched element
    result = insertElementMongoDB(collection, latest)
    saveLog('fetch.py','Successfully inserted with ID: {0}'.format(result.inserted_id)+'\n')
    saveLog('fetch.py', "Percentuale dispositivi Samsung: %s" % str(samsung))
    saveLog('fetch.py', "Percentuale dispositivi Apple: %s" % str(apple))

    #Closing connection
    closeMongoDB(client)
