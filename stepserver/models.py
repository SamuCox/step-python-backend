# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# user id and the conditions (comparison: all/group, context: semantic/nonsemantic)
class User(models.Model):
	user_id = models.CharField(max_length=200)
	comparison = models.CharField(max_length=100)
	context = models.CharField(max_length=100)

class Stepcount(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField()
	step_count = models.IntegerField(default=0)

class Message(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	message_id = models.CharField(max_length=200)
	date = models.DateField()
