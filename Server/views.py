# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return HttpResponse("foo: %s, " % str(data["foo"]) + "bar: %s" % str(data["bar"]))
