# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import *
from database import *


"""
per collegarsi al db:

exec su kinect
mongo
use SpyTorch
db.aggregate.find() per vedere tutto
"""

def responseTest(data):
    client = MongoClient("localhost", 32775)
    db = client.SpyTorch
    collection = db.aggregate

    result = collection.insert_one(data)
    strReturn = 'Successfully inserted, with ID: {0}'.format(result.inserted_id)

    client.close()

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
