from __future__ import unicode_literals
import json
import datetime
from django.http import JsonResponse, HttpResponse
from bson import BSON, json_util

from database import *
from fetch import fetchData
from logs import saveLog

def responseTest(data):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)

    #Add timestamp before fetching
    data["date"] = datetime.datetime.now()

    #Fetch data for multiple purpose
    fetchData(data)

    result = insertElementMongoDB(collection, data)
    strReturn = 'Successfully inserted, with ID: {0}'.format(result.inserted_id)
    saveLog("request.py",strReturn)

    closeMongoDB(client)

    return strReturn

def returnAllDevices():
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client, DBFETCHNAME)

    result = {}
    result['response'] = True
    #Select latest element
    result["devicesList"] = json_util.dumps(selectLatestNElementsMongoDB(collection, 1))

    closeMongoDB(client)

    return result


def IMEIwithSlug(slug):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client, DBFETCHNAME)

    result = {}
    result["response"] = True
    result["IMEIList"] = []
    allResult = selectLatestNElementsMongoDB(collection, 1)

    #    for devices in allResult:
    #        device = devices["stats"]["BuildInfo"]["Manufacturers"]["devices"]
    #        for brand in device:
    #            if brand["Brand"] == slug:
    #                result["IMEIList"] = brand

    for brand in allResult[0]["stats"]["BuildInfo"]["Manufacturers"]["devices"]:
        if brand["Brand"] == slug:
            result["IMEIList"] = brand

    if not result["IMEIList"]:
        result["response"] = False

    result["IMEIList"] = json_util.dumps(result["IMEIList"])
    closeMongoDB(client)

    return result


def UserWithSlug(slug):
    result = {}
    result["response"] = False
    result["UserList"] = selectUserWithSlug(slug)

    if result["UserList"]:
        result["response"] = True

    result["UserList"] = json_util.dumps(result["UserList"])

    return result


def AllUsers():
    result = {}
    result["response"] = False
    result["UserList"] = []
    tmpResult = selectAllUsers()

    for user in tmpResult:
        print user
        if user["UserInfo"]["Username"] in result["UserList"]:
            result["UserList"].append(user["UserInfo"]["Username"])

    if result["UserList"]:
        result["response"] = True

    result["UserList"] = json_util.dumps(result["UserList"])

    return result


def postRequest(request):
    data = json.loads(request.body)

    print data

    r = data["r"]
    print "request: "+r

    if r == "InsertDevice":
        response = responseTest(data)
    elif r == "WebAppAllDevices":
        response = returnAllDevices()
    elif r == "GetIMEIWithSlug":
        response = IMEIwithSlug(data["slug"])
    elif r == "GetUserWithSlug":
        response = UserWithSlug(data["slug"])
    elif r == "GetAllUsers":
        response = AllUsers()

    if response is None:
        response = 'errore'

    print "response: "
    print json.dumps(response)

    return response

def getRequest(request):
    return "GET Request with foo: " + request.GET.get('foo', '') + ' and bar: ' + request.GET.get('bar', '')
