from __future__ import unicode_literals
import datetime
from bson import BSON, json_util

from database import *
from fetch import *
from logs import saveLog


def InsertDevice(data):
    #Add timestamp before fetching
    data["date"] = datetime.datetime.now()

    result = insertElementMongoDB(data)
    strReturn = 'Successfully inserted, with ID: {0}'.format(result.inserted_id)
    saveLog("request.py",strReturn)

    return strReturn

def returnAllDevices():
    result = {}
    result['response'] = True

    # Select all elements
    allResult = selectLatestNElementsMongoDB(0)
    print allResult

    devicesList = []

    # map device[brand] in devicesList->device[brand]
    for device in allResult:
        if (not devicesList) or (not filter(lambda x: x["Brand"] == device["BuildInfo"]["Manufacturer"], devicesList)):
            devicesList.append(
                {"Brand": device["BuildInfo"]["Manufacturer"], "IMEI": [device["TelephoneInfo"]["IMEI"]], "counter": 1})
        else:
            map(lambda x: x["IMEI"].append(device["TelephoneInfo"]["IMEI"]), (filter(
                lambda x: (x["Brand"] == device["BuildInfo"]["Manufacturer"]) and (
                not device["TelephoneInfo"]["IMEI"] in x["IMEI"]), devicesList)))

    for device in devicesList:
        device["counter"] = len(device["IMEI"])

    result["devicesList"] = json_util.dumps(devicesList)

    return result

def IMEIwithSlug(slug):
    result = {}
    result["response"] = True
    result["IMEIList"] = []
    allResult = selectLatestNElementsMongoDB(0)

    devicesList = []

    # map device[brand] in devicesList->device[brand]
    for device in allResult:
        if (not devicesList) or (not filter(lambda x: x["Brand"] == device["BuildInfo"]["Manufacturer"], devicesList)):
            devicesList.append(
                {"Brand": device["BuildInfo"]["Manufacturer"], "IMEI": [device["TelephoneInfo"]["IMEI"]],
                 "Model": device["BuildInfo"]["Model"], "counter": 1})
        else:
            map(lambda x: x["IMEI"].append(device["TelephoneInfo"]["IMEI"]),
                (filter(lambda x: (x["Brand"] == device["BuildInfo"]["Manufacturer"]) and (
                not device["TelephoneInfo"]["IMEI"] in x["IMEI"]), devicesList)))

    for device in devicesList:
        device["counter"] = len(device["IMEI"])

        if device["Brand"] == slug:
            result["IMEIList"] = device

    result["devicesList"] = json_util.dumps(devicesList)

    if not result["IMEIList"]:
        result["response"] = False

    result["IMEIList"] = json_util.dumps(result["IMEIList"])

    return result


def UserWithSlug(slug):
    result = {}
    result["response"] = False
    allResult = selectUserWithSlug(slug)
    userList = []

    for device in allResult:
        if (not userList) or (
        not filter(lambda x: x["TelephoneInfo"]["IMEI"] == device["TelephoneInfo"]["IMEI"], userList)):
            userList.append(device)
        else:
            if (filter(lambda x: (x["TelephoneInfo"]["IMEI"] == device["TelephoneInfo"]["IMEI"]) and (
            not device["TelephoneInfo"]["IMEI"] in x["TelephoneInfo"]["IMEI"]), userList)):
                # if imei isn't alredy inserted
                userList.append(device)

    result["UserList"] = json_util.dumps(userList)

    if result["UserList"]:
        result["response"] = True

    return result


def AllUsers():
    result = {}
    result["response"] = False
    userList = []
    tmpResult = selectAllUsers()

    for user in tmpResult:
        if (not userList) or (not filter(lambda x: x == user["UserInfo"]["Username"], userList)):
            userList.append(user["UserInfo"]["Username"])

    result["UserList"] = json_util.dumps(userList)

    if result["UserList"]:
        result["response"] = True

    return result


def DevicesWithSlug(slug):
    result = {}
    result["response"] = True
    result["DevicesList"] = json_util.dumps(selectDevicesWithSlug(slug))

    if not result["DevicesList"]:
        result["response"] = False

    return result


def PushTheMessage(message):
    # {u'Message': {u'Username': u'Sconosciuto', u'Text': u'Ciaone', u'Sender': u'15555215554', u'ReceiverNumber': u'3482706721'}, u'r': u'pushMessageOut'}
    result = {}
    result["response"] = True

    messageList = {"MessageUsername": message["Username"], "sender": message["Sender"],
                   "receiver": message["ReceiverNumber"], "text": message["Text"], "IMEI": message["IMEI"]}
    insertMessageList(messageList)


    return message


def AllMessagesWithIMEI(slug):
    response = {}
    response['response'] = True
    response["MessagesList"] = json_util.dumps(selectMessagesList(slug))

    return response


def AllDevices():
    response = {}
    response['response'] = True
    allResult = selectAllDevices()
    devicesList = []

    for device in allResult:
        if (not devicesList) or (
        not filter(lambda x: x["TelephoneInfo"]["IMEI"] == device["TelephoneInfo"]["IMEI"], devicesList)):
            devicesList.append(device)
        else:
            map(lambda x: devicesList.append(x), filter(
                lambda x: (x["TelephoneInfo"]["IMEI"] == device["TelephoneInfo"]["IMEI"]) and (
                not device["TelephoneInfo"]["IMEI"] in x["TelephoneInfo"]["IMEI"]), devicesList))

    response["DevicesList"] = json_util.dumps(devicesList)

    return response


def BrandStats():
    response = {}
    response["response"] = True
    devicesList = []

    allResult = selectAllDevices()

    # map device[brand] in devicesList->device[brand]
    for device in allResult:
        if (not devicesList) or (not filter(lambda x: x["Brand"] == device["BuildInfo"]["Manufacturer"], devicesList)):
            devicesList.append({"Brand": device["BuildInfo"]["Manufacturer"], "IMEI": [device["TelephoneInfo"]["IMEI"]],
                                "Model": device["BuildInfo"]["Model"], "counter": 1})
        else:
            map(lambda x: x["IMEI"].append(device["TelephoneInfo"]["IMEI"]),
                (filter(lambda x: (x["Brand"] == device["BuildInfo"]["Manufacturer"]) and (
                    not device["TelephoneInfo"]["IMEI"] in x["IMEI"]), devicesList)))

        for device in devicesList:
            device["counter"] = len(device["IMEI"])

    response["DevicesList"] = json_util.dumps(devicesList)

    return response


def AndroidVersionStats():
    response = {}
    response["response"] = True

    devicesList = []

    allResult = selectAllDevices()

    # map device[brand] in devicesList->device[brand]
    for device in allResult:
        if (not devicesList) or (not filter(lambda x: x["AndroidVersion"] == getAndroidVersion(device), devicesList)):
            devicesList.append(
                {"AndroidVersion": getAndroidVersion(device), "IMEI": [device["TelephoneInfo"]["IMEI"]], "counter": 1})
        else:
            map(lambda x: x["IMEI"].append(device["TelephoneInfo"]["IMEI"]),
                (filter(lambda x: (x["AndroidVersion"] == getAndroidVersion(device)) and (
                not device["TelephoneInfo"]["IMEI"] in x["IMEI"]), devicesList)))

        for device in devicesList:
            device["counter"] = len(device["IMEI"])

    response["AndroidVersionList"] = json_util.dumps(devicesList)

    return response


def BatteryStatsWithIMEI(slug):
    response = {}
    response['response'] = True
    response["all"] = []
    tmpResult = selectDevicesWithSlug(slug)

    all = [{"value": '00', "counter": 0, "battery": 0}, {"value": '01', "counter": 0, "battery": 0},
           {"value": '02', "counter": 0, "battery": 0},
           {"value": '03', "counter": 0, "battery": 0},
           {"value": '04', "counter": 0, "battery": 0}, {"value": '05', "counter": 0, "battery": 0},
           {"value": '06', "counter": 0, "battery": 0},
           {"value": '07', "counter": 0, "battery": 0},
           {"value": '08', "counter": 0, "battery": 0}, {"value": '09', "counter": 0, "battery": 0},
           {"value": '10', "counter": 0, "battery": 0},
           {"value": '11', "counter": 0, "battery": 0},
           {"value": '12', "counter": 0, "battery": 0}, {"value": '13', "counter": 0, "battery": 0},
           {"value": '14', "counter": 0, "battery": 0},
           {"value": '15', "counter": 0, "battery": 0},
           {"value": '16', "counter": 0, "battery": 0}, {"value": '17', "counter": 0, "battery": 0},
           {"value": '18', "counter": 0, "battery": 0},
           {"value": '19', "counter": 0, "battery": 0},
           {"value": '20', "counter": 0, "battery": 0}, {"value": '21', "counter": 0, "battery": 0},
           {"value": '22', "counter": 0, "battery": 0},
           {"value": '23', "counter": 0, "battery": 0}
           ];

    for device in tmpResult:
        for hour in all:
            # se il documento rientra nelle ultime 24 ore
            if (getHourByDate(str(device["date"])) == hour["value"] and hour["counter"] < 1) and (
            todayDay(device["date"])):
                hour["counter"] += 1
                hour["battery"] = device["BatteryInfo"]["Level"]

    for hour in all:
        response["all"].append(hour["battery"])

    return response



def postRequest(request):
    data = json.loads(request.body)
    response = None

    print data

    r = data["r"]
    print "request: "+r

    if r == "InsertDevice":
        response = InsertDevice(data)
    elif r == "WebAppAllDevices":
        response = returnAllDevices()
    elif r == "GetIMEIWithSlug":
        response = IMEIwithSlug(data["slug"])
    elif r == "GetUserWithSlug":
        response = UserWithSlug(data["slug"])
    elif r == "GetAllUsers":
        response = AllUsers()
    elif r == "GetDevicesWithSlug":
        response = DevicesWithSlug(data["slug"])
    elif r == "pushMessage":
        response = PushTheMessage(data["Message"])
    elif r == "GetMessagesWithIMEI":
        response = AllMessagesWithIMEI(data["slug"])
    elif r == "GetAllDevices":
        response = AllDevices()
    elif r == "AndroidVersionStats":
        response = AndroidVersionStats()
    elif r == "BrandStats":
        response = BrandStats()
    elif r == "GetBatteryStatsWithIMEI":
        response = BatteryStatsWithIMEI(data["slug"])

    if response is None:
        response["response"] = 'errore'

    print "response: "
    print json.dumps(response)

    return response

def getRequest(request):
    return "GET Request with foo: " + request.GET.get('foo', '') + ' and bar: ' + request.GET.get('bar', '')
