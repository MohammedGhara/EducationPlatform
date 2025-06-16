from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

class Person(models.Model):
    name = models.CharField(max_length=100)
    marks = models.CharField(max_length=100)

class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(max_length=100)
