# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class User(models.Model):
    location = models.CharField(max_length=256)
    email = models.CharField(max_length=256)

    
