from __future__ import unicode_literals
import json
import datetime

from database import *


def responseTest(data):
    client = connectMongoDB()
    collection = selectCollectionMongoDB(client)

    data["date"] = datetime.datetime.now()

    result = insertElementMongoDB(collection, data)
    strReturn = 'Successfully inserted, with ID: {0}'.format(result.inserted_id)

    closeMongoDB(client)

    return strReturn


def postRequest(request):
    data = json.loads(request.body)
    response = responseTest(data)

    if response is None:
        response = 'errore'

    return response


def getRequest(request):
    return "GET Request with foo: " + request.GET.get('foo', '') + ' and bar: ' + request.GET.get('bar', '')
