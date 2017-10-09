# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests


@csrf_exempt
def index(request):
    if request.method == "POST":
        r = requests.Requests(request)
        response = r.postRequest(request)
        return JsonResponse(response, safe=False)

    elif request.method == "GET":
        response = r.getRequest(request)
        return HttpResponse("Response: %s" % str(response))

    else:
        return HttpResponse("Anything else response")
