from __future__ import unicode_literals
from bson import json_util
import datetime
import json

import database
import fetch
import logs
import messages
import responses

from Queue import Queue
from threading import Thread

NUM_WORKERS = 4
task_queue = Queue()
# Initialize user list
listina = []

class Requests:
    req = any

    # constructor
    def __init__(self, req, opt="POST"):
        if opt == "POST":
            self.req = json.loads(req.body)
        else:
            self.req = req

    # getters
    def getBody(self):
        return self.req

    def getReq(self, r):
        return r["r"]

    # methods
    def InsertDevice(self, data):
        # Initialize response
        response = responses.Responses()

        # Add timestamp before fetching
        data["date"] = datetime.datetime.now()

        # Insert device into database
        result = database.insertElementMongoDB(data)

        # Save id into log file
        strReturn = 'Successfully inserted, with ID: {0}'.format(result.inserted_id)
        logs.saveLog("request.py", strReturn)

        # Set and return success message
        response.setResponse("response", True)
        response.setResponse("Message", "Successfully inserted")
        return response

    def returnAllDevices(self):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", False)

        # Select all elements in database
        allResult = database.selectLatestNElementsMongoDB(0)

        # Initialize devices list
        devicesList = []

        devicesList = fetch.processDevicesList(allResult, devicesList)

        # Set True response if devicesList is not empty
        if devicesList:
            response.setResponse("response", True)

        # Set and return response
        response.setResponse("devicesList", json_util.dumps(devicesList))
        return response

    def IMEIwithSlug(self, slug):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", False)

        # Select all elements in database
        allResult = database.selectLatestNElementsMongoDB(0)

        # Initialize devices list and IMEIList
        devicesList = []
        IMEIList = []

        devicesList = fetch.processDevicesList(allResult, devicesList)

        # For every device in devicesList, if it's the same brand name, push into the IMEIList
        for device in devicesList:
            if device["Brand"] == slug:
                IMEIList = device

        # If IMEIList is not empty
        if IMEIList:
            response.setResponse("response", True)

        # Set and return response
        response.setResponse("devicesList", json_util.dumps(devicesList))
        response.setResponse("IMEIList", json_util.dumps(IMEIList))
        return response

    def UserWithSlug(self, slug):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", False)

        # Initialize devices list
        userList = []

        # Select all users with those slug in database
        allResult = database.selectUserWithSlug(slug)

        # Select and map only physical devices (without duplicate entry)
        map(lambda x: fetch.mapIMEIinDevice(userList, x), allResult)

        # If userList is not empty
        if json_util.dumps(userList):
            response.setResponse("response", True)

        # Set and return response
        response.setResponse("UserList", json_util.dumps(userList))
        return response

    def worker(self):
        # Constantly check the queue for addresses
        while True:
            user = task_queue.get()

            if (not listina) or (not filter(lambda x: x == user, listina)):
                listina.append(user)

            # Mark the processed task as done
            task_queue.task_done()

    def AllUsers(self):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", False)

        # Initialize user list
        userList = []

        # Select all users
        tmpResult = database.selectAllUsers()

        # Per ogni risultato di tmpResult, creare un thread
        threads = [Thread(target=self.worker) for _ in range(NUM_WORKERS)]

        # Add the websites to the task queue
        [task_queue.put(user["UserInfo"]["Username"]) for user in tmpResult]

        # Start all the workers
        [thread.start() for thread in threads]

        # Wait for all the tasks in the queue to be processed
        task_queue.join()

        # If userList is not empty
        if json_util.dumps(listina):
            response.setResponse("response", True)

        # Set and return response
        response.setResponse("UserList", json_util.dumps(listina))
        return response

    def DevicesWithSlug(self, IMEI):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", False)

        # Select all info for a device with selected IMEI
        allResult = json_util.dumps(database.selectDevicesWithSlug(IMEI))

        # If device exist
        if allResult:
            response.setResponse("response", True)
            response.setResponse("DevicesList", allResult)

        # Return response
        return response


    def PushTheMessage(self, message):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", True)

        # Create new message 'm' with all field setted
        m = messages.Messages(message["Username"], message["Sender"], message["ReceiverNumber"], message["Text"],
                              message["IMEI"])

        # Convert 'm' object into JSON
        messageList = m.createJson()

        # Insert the message into database
        database.insertMessageList(messageList)

        # Just for debug
        print m.getSender() + " ha inviato a " + m.getReceiver() + ": " + m.getText()

        # Return response
        return response

    def AllMessagesWithIMEI(self, slug):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", True)

        # Insert into MessagesList all message for a device
        response.setResponse("MessagesList", json_util.dumps(database.selectMessagesList(slug)))

        # Return response
        return response

    def AllDevices(self):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", True)

        # Select all devices into database
        allResult = database.selectAllDevices()

        # Initialize devices list
        devicesList = []

        # Select and map only physical devices (without duplicate entry)
        map(lambda x: fetch.mapIMEIinDevice(devicesList, x), allResult)

        # Set and return response
        response.setResponse("DevicesList", json_util.dumps(devicesList))
        return response


    def BrandStats(self):

        response = responses.Responses()
        response.setResponse("response", True)
        devicesList = []

        allResult = database.selectAllDevices()

        devicesList = fetch.processDevicesList(allResult, devicesList)

        response.setResponse("DevicesList", json_util.dumps(devicesList))
        return response


    def AndroidVersionStats(self):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", True)

        # Initialize devices list
        devicesList = []

        # Select all result from database
        allResult = database.selectAllDevices()

        # For every device in database, if devicesList is empty or don't contain that Android version, push that device
        # in new brand document first and then in devicesList, else push that Android version in correct brand document
        # first and then in devicesList
        for device in allResult:
            if (not devicesList) or (
                    not filter(lambda x: x["AndroidVersion"] == fetch.getAndroidVersion(device), devicesList)):
                devicesList.append(
                    {"AndroidVersion": fetch.getAndroidVersion(device), "IMEI": [device["TelephoneInfo"]["IMEI"]],
                     "counter": 1})
            else:
                map(lambda x: x["IMEI"].append(device["TelephoneInfo"]["IMEI"]),
                    (filter(lambda x: (x["AndroidVersion"] == fetch.getAndroidVersion(device)) and (
                        not device["TelephoneInfo"]["IMEI"] in x["IMEI"]), devicesList)))

            for device in devicesList:
                device["counter"] = len(device["IMEI"])

        # Set and return response
        response.setResponse("AndroidVersionList", json_util.dumps(devicesList))
        return response


    def BatteryStatsWithIMEI(self, slug):

        # Initialize response
        response = responses.Responses()
        response.setResponse("response", True)

        # Initialize lists
        allResp = []
        h = []

        # Select all from database for that device
        tmpResult = database.selectDevicesWithSlug(slug)

        # Initialize allResp list with hours document
        for x in xrange(0, 23):
            if x < 10:
                allResp.append({"value": "0" + str(x), "counter": 0, "battery": 0})
            else:
                allResp.append({"value": str(x), "counter": 0, "battery": 0})

        # For every device in database, for every hour, if we have some battery usage for today, fill hour list
        for device in tmpResult:
            for hour in allResp:
                # se il documento rientra nelle ultime 24 ore
                if (fetch.getHourByDate(str(device["date"])) == hour["value"]) and hour["counter"] < 1 and (
                        fetch.todayDay(device["date"])):
                    hour["counter"] += 1
                    hour["battery"] = device["BatteryInfo"]["Level"]

                h.append(hour["battery"])

        # If we had battery usage
        if h:
            response.setResponse("all", h)

        # Return response
        return response

    def postRequest(self):

        # Initialize response
        response = responses.Responses()

        # Grub body from request
        data = self.getBody()

        # Grub request from body
        r = self.getReq(data)
        print "request: " + r

        # Switch 'r' for every possible request
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

        # If we haven't a response
        if not response.getResponse():
            response.setResponse("reponse", False)
            response.setResponse("Message", "Qualcosa e' andato storto")

        # Return the response
        return response.getResponse()

    def getRequest(self, request):
        return "GET Request with foo: " + request.GET.get('foo', '') + ' and bar: ' + request.GET.get('bar', '')
