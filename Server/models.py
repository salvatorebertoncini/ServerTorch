# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from mongoengine import *


class Data(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
