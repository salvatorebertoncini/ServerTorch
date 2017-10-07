from database import *
from logs import saveLog
import time, datetime
import re

#JSON Example
#{ "date": "", "stats": {"BuildInfo": {"Manufacturers": { "devices": [{"Brand": "Samsung","IMEI" : ["1012021002", "1283298372"],	"counter": 2},{	"Brand": "Huawei","IMEI" : ["12382121321", "213213211", "29183120938721"],"counter": 3}	],"totalCounter": 5 } },"flag": true }}

epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000


def todayDay(slug):
    millis = int(round(time.time() * 1000))
    if unix_time_millis(slug) - millis < 86400000:
        return True
    else:
        return False



def getDate(date):
    regex = r"(\d.*?) "
    test_str = date

    matches = re.finditer(regex, test_str)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            return match.group(groupNum)


def getHourByDate(date):
    regex = r" (\d.*?):"
    test_str = date

    matches = re.finditer(regex, test_str)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            return match.group(groupNum)

def getAndroidVersion(device):
    regex = r":(\d.*?)/"
    test_str = device["BuildInfo"]["Fingerprint"]

    matches = re.finditer(regex, test_str)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            return match.group(groupNum)


def ManufacturerFetch(device, imei, deviceList):
    if (not deviceList["devices"]) or (not filter(lambda x: x["Brand"] == device, deviceList["devices"])):
        counter = 1
        deviceList["devices"].append({"IMEI": [imei], "Brand": device, "counter": counter})
        deviceList["totalCounter"] += 1

    else:
        #append and couter++ into foreach loop
        for d in deviceList["devices"]:
            if d["Brand"] == device:
                # if imei isn't alredy inserted
                if not imei in d["IMEI"]:
                    d["IMEI"].append(imei)
                    d["counter"] += 1
                    deviceList["totalCounter"] += 1

    return deviceList

def DevicePercentage(device, deviceList):
    if (not deviceList["devices"]) or (not filter(lambda x: x["Brand"] == device, deviceList["devices"])):
        return 0
    else:
        #return device percentage, i.e. (counter/totalCounter)*100
        return ( map(lambda x: x["counter"], filter(lambda x: x["Brand"] == device, deviceList["devices"]))[0] *100)  / deviceList["totalCounter"]

def fetchData(data):
    #Select latest element
    latest = selectLatestNElementsMongoDB(1)

    #Fetch Manufacturer
    BuildInfoList = latest[0]["stats"]["BuildInfo"]["Manufacturers"]
    BuildInfoList = ManufacturerFetch(data["BuildInfo"]["Manufacturer"], data["TelephoneInfo"]["IMEI"], BuildInfoList)

    #e.g. percentage of Samsung devices in the database
    samsung = DevicePercentage("Samsung", BuildInfoList)
    htc = DevicePercentage("HTC", BuildInfoList)
    apple = DevicePercentage("Apple Inc.", BuildInfoList)

    #Insert new results
    latest = { "date": datetime.datetime.now(), "stats": {"BuildInfo": {"Manufacturers": BuildInfoList}},"flag": True }

    #Save fetched element
    result = insertElementMongoDB(latest)
    saveLog('fetch.py','Successfully inserted with ID: {0}'.format(result.inserted_id)+'\n')

    print "Percentuale dispositivi Samsung: %s " % str(samsung)
    print "Percentuale dispositivi HTC: %s " % str(htc)
    print "Percentuale dispositivi Apple: %s " % str(apple)

