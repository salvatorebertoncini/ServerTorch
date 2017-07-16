# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from pymongo import *
from database import *


def responseTest(data):
    client = connectMongoDB()
    db = client.SpyTorch
    #db = client.DBNAME
    collection = db.aggregate

    data["date"] = datetime.datetime.now()
    result = collection.insert_one(data)
    strReturn = 'Successfully inserted, with ID: {0}'.format(result.inserted_id)

    closeMongoDB(client)

    return strReturn

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = responseTest(data)

        #response = data

        if response is None:
            response = 'errore'

        return HttpResponse("Response: %s" % str(response))

    elif request.method == "GET":
        return HttpResponse("GET Request with foo: " + request.GET.get('foo', '') + ' and bar: ' + request.GET.get('bar', ''))

    else:
        return HttpResponse("Anything else response")
