from __future__ import unicode_literals
import datetime
from bson import BSON, json_util

from database import *
from fetch import *
from logs import saveLog

import messages
import responses


class Requests:
    req = any

    # constructor
    def __init__(self, req):
        self.req = json.loads(req.body)

    # getters
    def getBody(self):
        return self.req

    def getReq(self, r):
        return r["r"]

    # methods
    def InsertDevice(self, data):
        response = responses.Responses()

        # Add timestamp before fetching
        data["date"] = datetime.datetime.now()

        result = insertElementMongoDB(data)
        strReturn = 'Successfully inserted, with ID: {0}'.format(result.inserted_id)
        saveLog("request.py", strReturn)

        response.setResponse("response", True)
        response.setResponse("Message", strReturn)

        return response

    def returnAllDevices(self):

        response = responses.Responses()
        response.setResponse("response", True)

        # Select all elements
        allResult = selectLatestNElementsMongoDB(0)

        devicesList = []

        # map device[brand] in devicesList->device[brand]
        for device in allResult:
            if (not devicesList) or (
            not filter(lambda x: x["Brand"] == device["BuildInfo"]["Manufacturer"], devicesList)):
                devicesList.append(
                    {"Brand": device["BuildInfo"]["Manufacturer"], "IMEI": [device["TelephoneInfo"]["IMEI"]],
                     "counter": 1})
            else:
                map(lambda x: x["IMEI"].append(device["TelephoneInfo"]["IMEI"]), (filter(
                    lambda x: (x["Brand"] == device["BuildInfo"]["Manufacturer"]) and (
                        not device["TelephoneInfo"]["IMEI"] in x["IMEI"]), devicesList)))

        for device in devicesList:
            device["counter"] = len(device["IMEI"])

        response.setResponse("devicesList", json_util.dumps(devicesList))

        return response

    def IMEIwithSlug(self, slug):

        response = responses.Responses()
        response.setResponse("response", True)

        result = {}
        result["response"] = True
        result["IMEIList"] = []
        allResult = selectLatestNElementsMongoDB(0)

        devicesList = []

        # map device[brand] in devicesList->device[brand]
        for device in allResult:
            if (not devicesList) or (
            not filter(lambda x: x["Brand"] == device["BuildInfo"]["Manufacturer"], devicesList)):
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

        response.setResponse("devicesList", json_util.dumps(devicesList))
        response.setResponse("IMEIList", json_util.dumps(result["IMEIList"]))

        if not result["IMEIList"]:
            response.setResponse("response", False)

        return response

    def UserWithSlug(self, slug):

        response = responses.Responses()
        response.setResponse("response", False)
        userList = []

        allResult = selectUserWithSlug(slug)

        map(lambda x: self.mapIMEIinDevice(userList, x), allResult)

        response.setResponse("UserList", json_util.dumps(userList))

        if json_util.dumps(userList):
            response.setResponse("response", True)

        return response

    def mapIMEIinDevice(self, userList, device):
        if (not userList) or (
                not filter(lambda x: x["TelephoneInfo"]["IMEI"] == device["TelephoneInfo"]["IMEI"], userList)):
            userList.append(device)
        else:
            if (filter(lambda x: (x["TelephoneInfo"]["IMEI"] == device["TelephoneInfo"]["IMEI"]) and (
                    not device["TelephoneInfo"]["IMEI"] in x["TelephoneInfo"]["IMEI"]), userList)):
                # if imei isn't alredy inserted
                userList.append(device)

    def AllUsers(self):

        response = responses.Responses()
        response.setResponse("response", False)
        userList = []
        tmpResult = selectAllUsers()

        for user in tmpResult:
            if (not userList) or (not filter(lambda x: x == user["UserInfo"]["Username"], userList)):
                userList.append(user["UserInfo"]["Username"])

        response.setResponse("UserList", json_util.dumps(userList))

        if json_util.dumps(userList):
            response.setResponse("response", True)

        return response

    def DevicesWithSlug(self, slug):

        response = responses.Responses()

        if not json_util.dumps(selectDevicesWithSlug(slug)):
            response.setResponse("response", False)
        else:
            response.setResponse("response", True)
            response.setResponse("DevicesList", json_util.dumps(selectDevicesWithSlug(slug)))

        return response

    def PushTheMessage(self, message):
        # {u'Message': {u'Username': u'Sconosciuto', u'Text': u'Ciaone', u'Sender': u'15555215554', u'ReceiverNumber': u'3482706721'}, u'r': u'pushMessageOut'}
        response = responses.Responses()
        response.setResponse("response", True)

        m = messages.Messages(message["Username"], message["Sender"], message["ReceiverNumber"], message["Text"],
                              message["IMEI"])
        messageList = m.createJson()
        insertMessageList(messageList)

        print m.getSender() + " ha inviato a " + m.getReceiver() + ": " + m.getText()

        return response

    def AllMessagesWithIMEI(self, slug):
        response = responses.Responses()

        response.setResponse("response", True)
        response.setResponse("MessagesList", json_util.dumps(selectMessagesList(slug)))

        return response

    def AllDevices(self):
        response = responses.Responses()
        response.setResponse("response", True)

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

        response.setResponse("DevicesList", json_util.dumps(devicesList))

        return response

    def BrandStats(self):

        response = responses.Responses()
        response.setResponse("response", True)
        devicesList = []

        allResult = selectAllDevices()

        # map device[brand] in devicesList->device[brand]
        for device in allResult:
            if (not devicesList) or (
            not filter(lambda x: x["Brand"] == device["BuildInfo"]["Manufacturer"], devicesList)):
                devicesList.append(
                    {"Brand": device["BuildInfo"]["Manufacturer"], "IMEI": [device["TelephoneInfo"]["IMEI"]],
                     "Model": device["BuildInfo"]["Model"], "counter": 1})
            else:
                map(lambda x: x["IMEI"].append(device["TelephoneInfo"]["IMEI"]),
                    (filter(lambda x: (x["Brand"] == device["BuildInfo"]["Manufacturer"]) and (
                        not device["TelephoneInfo"]["IMEI"] in x["IMEI"]), devicesList)))

            for device in devicesList:
                device["counter"] = len(device["IMEI"])

        response.setResponse("DevicesList", json_util.dumps(devicesList))

        return response

    def AndroidVersionStats(self):

        response = responses.Responses()
        response.setResponse("response", True)
        devicesList = []

        allResult = selectAllDevices()

        # map device[brand] in devicesList->device[brand]
        for device in allResult:
            if (not devicesList) or (
            not filter(lambda x: x["AndroidVersion"] == getAndroidVersion(device), devicesList)):
                devicesList.append(
                    {"AndroidVersion": getAndroidVersion(device), "IMEI": [device["TelephoneInfo"]["IMEI"]],
                     "counter": 1})
            else:
                map(lambda x: x["IMEI"].append(device["TelephoneInfo"]["IMEI"]),
                    (filter(lambda x: (x["AndroidVersion"] == getAndroidVersion(device)) and (
                        not device["TelephoneInfo"]["IMEI"] in x["IMEI"]), devicesList)))

            for device in devicesList:
                device["counter"] = len(device["IMEI"])

        response.setResponse("AndroidVersionList", json_util.dumps(devicesList))

        return response

    def BatteryStatsWithIMEI(self, slug):

        response = responses.Responses()
        response.setResponse("response", True)
        h = []

        tmpResult = selectDevicesWithSlug(slug)

        allResp = [{"value": '00', "counter": 0, "battery": 0},
                   {"value": '01', "counter": 0, "battery": 0},
                   {"value": '02', "counter": 0, "battery": 0},
                   {"value": '03', "counter": 0, "battery": 0},
                   {"value": '04', "counter": 0, "battery": 0},
                   {"value": '05', "counter": 0, "battery": 0},
                   {"value": '06', "counter": 0, "battery": 0},
                   {"value": '07', "counter": 0, "battery": 0},
                   {"value": '08', "counter": 0, "battery": 0},
                   {"value": '09', "counter": 0, "battery": 0},
                   {"value": '10', "counter": 0, "battery": 0},
                   {"value": '11', "counter": 0, "battery": 0},
                   {"value": '12', "counter": 0, "battery": 0},
                   {"value": '13', "counter": 0, "battery": 0},
                   {"value": '14', "counter": 0, "battery": 0},
                   {"value": '15', "counter": 0, "battery": 0},
                   {"value": '16', "counter": 0, "battery": 0},
                   {"value": '17', "counter": 0, "battery": 0},
                   {"value": '18', "counter": 0, "battery": 0},
                   {"value": '19', "counter": 0, "battery": 0},
                   {"value": '20', "counter": 0, "battery": 0},
                   {"value": '21', "counter": 0, "battery": 0},
                   {"value": '22', "counter": 0, "battery": 0},
                   {"value": '23', "counter": 0, "battery": 0}
                   ];

        for device in tmpResult:
            for hour in allResp:
                # se il documento rientra nelle ultime 24 ore
                if (getHourByDate(str(device["date"])) == hour["value"]) and hour["counter"] < 1 and (
                todayDay(device["date"])):
                    hour["counter"] += 1
                    hour["battery"] = device["BatteryInfo"]["Level"]

                h.append(hour["battery"])

        if h:
            response.setResponse("all", h)

        return response

    def postRequest(self, request):

        response = responses.Responses()

        data = self.getBody()

        r = self.getReq(data)
        print "request: " + r

        if r == "InsertDevice":
            response = self.InsertDevice(data)
        elif r == "WebAppAllDevices":
            response = self.returnAllDevices()
        elif r == "GetIMEIWithSlug":
            response = self.IMEIwithSlug(data["slug"])
        elif r == "GetUserWithSlug":
            response = self.UserWithSlug(data["slug"])
        elif r == "GetAllUsers":
            response = self.AllUsers()
        elif r == "GetDevicesWithSlug":
            response = self.DevicesWithSlug(data["slug"])
        elif r == "pushMessage":
            response = self.PushTheMessage(data["Message"])
        elif r == "GetMessagesWithIMEI":
            response = self.AllMessagesWithIMEI(data["slug"])
        elif r == "GetAllDevices":
            response = self.AllDevices()
        elif r == "AndroidVersionStats":
            response = self.AndroidVersionStats()
        elif r == "BrandStats":
            response = self.BrandStats()
        elif r == "GetBatteryStatsWithIMEI":
            response = self.BatteryStatsWithIMEI(data["slug"])

        print "response: "
        print response.getResponse()

        if not response.getResponse():
            response.setResponse("reponse", False)
            response.setResponse("Message", "Qualcosa e' andato storto")

        return response.getResponse()

    def getRequest(self, request):
        return "GET Request with foo: " + request.GET.get('foo', '') + ' and bar: ' + request.GET.get('bar', '')
