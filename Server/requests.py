from __future__ import unicode_literals
import datetime
from django.http import JsonResponse, HttpResponse
import json
from bson import BSON, json_util

from database import *
from fetch import fetchData
from logs import saveLog


def InsertDevice(data):
    #Add timestamp before fetching
    data["date"] = datetime.datetime.now()

    #Fetch data for multiple purpose
    # fetchData(data)

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
            for d in devicesList:
                if d["Brand"] == device["BuildInfo"]["Manufacturer"]:
                    # if imei isn't alredy inserted
                    if not device["TelephoneInfo"]["IMEI"] in d["IMEI"]:
                        d["IMEI"].append(device["TelephoneInfo"]["IMEI"])
                        d["counter"] += 1

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
                {"Brand": device["BuildInfo"]["Manufacturer"], "IMEI": [device["TelephoneInfo"]["IMEI"]], "counter": 1})
        else:
            for d in devicesList:
                if d["Brand"] == device["BuildInfo"]["Manufacturer"]:
                    # if imei isn't alredy inserted
                    if not device["TelephoneInfo"]["IMEI"] in d["IMEI"]:
                        d["IMEI"].append(device["TelephoneInfo"]["IMEI"])
                        d["counter"] += 1

    result["devicesList"] = json_util.dumps(devicesList)

    for brand in devicesList:
        if brand["Brand"] == slug:
            result["IMEIList"] = brand

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
            for d in userList:
                if d["TelephoneInfo"]["IMEI"] == device["TelephoneInfo"]["IMEI"]:
                    # if imei isn't alredy inserted
                    if not device["TelephoneInfo"]["IMEI"] in d["TelephoneInfo"]["IMEI"]:
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
    tmpResult = selectMessagesList(message["Username"])

    if not tmpResult:
        messageList = {"MessageUsername": "salvo.bertoncini", "MessageList": [
            {"sender": message["Sender"], "receiver": message["ReceiverNumber"], "text": message["Text"]}]}
        insertMessageList(messageList)
    else:
        tmpResult["MessageList"].append(
            {"sender": message["Sender"], "receiver": message["ReceiverNumber"], "text": message["Text"]})
        updateMessageList(tmpResult)
    return message


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


    if response is None:
        response = 'errore'

    print "response: "
    print json.dumps(response)

    return response

def getRequest(request):
    return "GET Request with foo: " + request.GET.get('foo', '') + ' and bar: ' + request.GET.get('bar', '')
