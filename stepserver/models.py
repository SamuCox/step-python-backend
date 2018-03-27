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

class Question(models.Model):
	section = models.CharField(max_length=200)
	category = models.CharField(max_length=200)
	#index inside the section
	index = models.IntegerField(default=0)
	content = models.CharField(max_length=10000)

class Option(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	content = models.CharField(max_length=10000)

class Streak(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	streak_id = models.IntegerField(default=0)
	start_date = models.DateField()
	end_date = models.DateField()
	median = models.IntegerField(default=0)
	n_active_day = models.IntegerField(default=0)
	n_inactive_day = models.IntegerField(default=0)
	p_500_5k = models.FloatField(default=0)
	p_5k_10k = models.FloatField(default=0)
	p_10k_105k = models.FloatField(default=0)
	p_105k = models.FloatField(default=0)
	slope = models.FloatField(default=0)
	cov = models.FloatField(default=0)
	autocorrelation = models.FloatField(default=0)
	trend = models.FloatField(default=0)
	skewness = models.FloatField(default=0)
	kurtosis = models.FloatField(default=0)
	days_since_last_prize = models.IntegerField(default=0)
	points_till_next_prize = models.IntegerField(default=0)


