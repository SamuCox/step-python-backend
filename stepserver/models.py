# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Stepcount(models.Model):
	user_id = models.CharField(max_length=200)
	date = models.DateField()
	step_count = models.IntegerField(default=0)