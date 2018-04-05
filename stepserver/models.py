# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date, datetime
from django.utils.timezone import localtime, now

# Create your models here.

# user id and the conditions (comparison: all/group, context: semantic/nonsemantic)
class User(models.Model):
	user_id = models.CharField(max_length=200)
	comparison = models.CharField(max_length=100)
	context = models.CharField(max_length=100)
	start_date = models.DateField(default=localtime(now()).date())

class Stepcount(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField(default=localtime(now()).date())
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
	user_cluster_id = models.IntegerField(default=0)
	streak_index = models.IntegerField(default=0)
	start_date = models.DateField(localtime(now()).date())
	end_date = models.DateField(localtime(now()).date())
	cohort_start_date = models.IntegerField(default=0)
	cohort_end_date = models.IntegerField(default=0)
	is_active = models.BooleanField(default=False)
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

class StreakGroupInfo(models.Model):
	name = models.CharField(max_length=200)
	color = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)
	step_level = models.CharField(max_length=100)
	duration = models.CharField(max_length=100)
	break_length = models.CharField(max_length=100)
	consistency = models.CharField(max_length=100)
	engagement = models.CharField(max_length=100)
	recommendation_id_ongoing = models.IntegerField(default=0)
	recommendation_id_upcoming = models.IntegerField(default=0)
	is_target_step_level = models.BooleanField(default=False)
	is_target_duration = models.BooleanField(default=False)
	is_target_break = models.BooleanField(default=False)
	is_target_consistency = models.BooleanField(default=False)
	is_target_engagement = models.BooleanField(default=False)
	has_bad_prediction = models.BooleanField(default=False)

class StreakInfo(models.Model):
	group = models.ForeignKey(StreakGroupInfo, on_delete=models.CASCADE)
	description = models.CharField(max_length=1000, blank=True, default="")
	step_level = models.CharField(max_length=100, blank=True, default="") #moderate, moderate high etc.
	duration = models.CharField(max_length=100, blank=True, default="")
	break_length = models.CharField(max_length=100, blank=True, default="")
	consistency = models.CharField(max_length=100, blank=True, default="")
	engagement = models.CharField(max_length=100, blank=True, default="")
	is_target_step_level = models.BooleanField(default=False)
	is_target_duration = models.BooleanField(default=False)
	is_target_break = models.BooleanField(default=False)
	is_target_consistency = models.BooleanField(default=False)
	is_target_engagement = models.BooleanField(default=False)
	has_bad_prediction = models.BooleanField(default=False)

# how to describe attributes / recommend improvement of attributes
class StreakAttributeDescription(models.Model):
	attribute = models.CharField(max_length=100)
	status = models.CharField(max_length=200)
	category = models.CharField(max_length=100) #description(how good or how bad) / recommendation in improvement
	content = models.CharField(max_length=1000)

class Challenge(models.Model):
	title = models.CharField(max_length=200)
	content = models.CharField(max_length=1000)
	difficulty = models.IntegerField(default=0)
	is_target_step_level = models.BooleanField(default=False)
	is_target_duration = models.BooleanField(default=False)
	is_target_break = models.BooleanField(default=False)
	is_target_consistency = models.BooleanField(default=False)
	is_target_engagement = models.BooleanField(default=False)

