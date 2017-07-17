import datetime

from database import *
from logs import saveLog

#JSON Example
#{ "date": "", "stats": {"BuildInfo": {"Manufacturer": [], "ManufacturerCounter": 0 }, "TelephoneInfo":  { "IMEIcounter": 0, "IMEIcollected": []} },"flag": true }


def ManufacturerFetch(device, imei, deviceList):

    if not filter(lambda x: x["Brand"] == device, deviceList["device"]):
        counter = 1
        deviceList["device"].append({"IMEI": [imei], "Brand": device, "counter": counter})
    else:
        #append and couter++ into foreach loop
        for d in deviceList["device"]:
            if d["Brand"] == device:
                d["IMEI"].append(imei)
                d["counter"] += 1

    deviceList["totalCounter"] += 1

    return deviceList


def DevicePercentage(device, deviceList):
    if filter(lambda x: x["Brand"] == device, deviceList["device"]):
        #return device percentage, i.e. (counter/totalCounter)*100
        return map(lambda x: (x["counter"] / deviceList["totalCounter"]) * 100, filter(lambda x: x["Brand"] == device, deviceList["device"]))
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

    #Insert new results
    latest = { "date": datetime.datetime.now(), "stats": {"BuildInfo": {"Manufacturer": BuildInfoList}},"flag": True }

    #Save fetched element
    result = insertElementMongoDB(collection, latest)
    saveLog('fetch.py','Successfully inserted with ID: {0}'.format(result.inserted_id)+'\n')

    print "Percentuale dispositivi Samsung: %s " % str(samsung)
    print "Percentuale dispositivi Apple: %s " % str(apple)

    #Closing connection
    closeMongoDB(client)
