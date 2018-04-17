import firebase_admin
from firebase_admin import credentials, db
from django.db.models import Q
from stepserver.models import Question, Option, Stepcount, Streak, StreakInfo, StreakGroupInfo, UserClusterInfo, UserClusterGroupInfo
from datetime import date
import datetime
import math

# Fetch the service account key JSON file contents
cred = credentials.Certificate('service-account-key.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://step-customer.firebaseio.com/'
	})

class MessageSender:

	def __init__(self, fb_db, dj_Q, md_Question, md_Option, md_Stepcount, md_Streak, md_Streakinfo, md_Streakgroupinfo, md_Userclusterinfo, md_Userclustergroupinfo, dt_date, dt_datetime, mt_math):
		self.fb_db = fb_db
		self.dj_Q = dj_Q
		self.md_Question = md_Question
		self.md_Option = md_Option
		self.md_Stepcount = md_Stepcount
		self.md_Streak = md_Streak
		self.md_Streakinfo = md_Streakinfo
		self.md_Streakgroupinfo = md_Streakgroupinfo
		self.md_Userclusterinfo = md_Userclusterinfo
		self.md_Userclustergroupinfo = md_Userclustergroupinfo
		self.dt_date = dt_date
		self.dt_datetime = dt_datetime
		self.mt_math = mt_math

	#take in uid, steps(?), date
	#require control grp info
	#graph: need no. of dates, content -> [need ctrl-grp to decide how many days to show & content (if streak): pull out the last/current streak; if not, show last WEEK]
	def generate_message(self):
		print()

	#cluster id: the targeted cluster id, streak id: recommendation
	#return an array of median steps

	def generate_comparison_calendar(self, streak_cluster_group_id, user_cluster_group_id, start_date, end_date, target, awareness):
		day = self.dt_datetime.timedelta(days=1)
		median_step_list = []
		single_date = start_date

		all_streak_clusters = self.md_Streakinfo.objects.filter(group_id=streak_cluster_group_id)
		all_user_clusters = self.md_Userclusterinfo.objects.filter(group_id=user_cluster_group_id)
		print("user cluster id: " + str(user_cluster_group_id))

		q_streak = self.dj_Q(pk=None)
		q_user = self.dj_Q(pk=None)
		# adding up all individuals under the group
		for streak_cluster in all_streak_clusters:
			print("streak cluster id: " + str(streak_cluster.id))
			q_streak = q_streak | self.dj_Q(streak_cluster_id=streak_cluster.id)
		for user_cluster in all_user_clusters:
			print("user cluster id: " + str(user_cluster.id))
			q_user = q_streak | self.dj_Q(user_cluster_id=user_cluster.id)

		while single_date <= end_date:
			if target == "group" and awareness == "streak":
				all_streaks = self.md_Streak.objects.filter(q_streak, q_user, calendar_date=single_date).order_by('step_count')
			elif target == "group" and awareness != "streak":
				all_streaks = self.md_Streak.objects.filter(q_user, calendar_date=single_date).order_by('step_count')
			elif target == "all" and awareness == "streak":
				all_streaks = self.md_Streak.objects.filter(q_streak, calendar_date=single_date).order_by('step_count')
			else:
				all_streaks = self.md_Streak.objects.filter(calendar_date=single_date).order_by('step_count')

			count = all_streaks.count()
			median = all_streaks[int(self.mt_math.floor(count/2))]
			median_step_list.append(median.step_count)
			single_date = single_date + day	
		return median_step_list

	def generate_comparison_cohort(self, streak_cluster_group_id, user_cluster_group_id, start_date, end_date, target, awareness):
		median_step_list = []
		single_date = start_date

		all_streak_clusters = self.md_Streakinfo.objects.filter(group_id=streak_cluster_group_id)
		all_user_clusters = self.md_Userclusterinfo.objects.filter(group_id=user_cluster_group_id)
		print("user cluster id: " + str(user_cluster_group_id))

		q_streak = self.dj_Q(pk=None)
		q_user = self.dj_Q(pk=None)
		# adding up all individuals under the group
		for streak_cluster in all_streak_clusters:
			print("streak cluster id: " + str(streak_cluster.id))
			q_streak = q_streak | self.dj_Q(streak_cluster_id=streak_cluster.id)
		for user_cluster in all_user_clusters:
			print("user cluster id: " + str(user_cluster.id))
			q_user = q_streak | self.dj_Q(user_cluster_id=user_cluster.id)

		while single_date <= end_date:
			if target == "group" and awareness == "streak":
				all_streaks = self.md_Streak.objects.filter(q_streak, q_user, cohort_day=single_date).order_by('step_count')
			elif target == "group" and awareness != "streak":
				all_streaks = self.md_Streak.objects.filter(q_user, cohort_day=single_date).order_by('step_count')
			elif target == "all" and awareness == "streak":
				all_streaks = self.md_Streak.objects.filter(q_streak, cohort_day=single_date).order_by('step_count')
			else:
				all_streaks = self.md_Streak.objects.filter(cohort_day=single_date).order_by('step_count')

			count = all_streaks.count()
			median = all_streaks[int(self.mt_math.floor(count/2))]
			median_step_list.append(median.step_count)
			single_date = single_date + 1
		return median_step_list

	def get_streak_start_date(self, streak):
		streak_index = streak.streak_index
		user = streak.user
		all_streaks = self.md_Streak.objects.filter(user=user, streak_index=streak_index).order_by('calendar_date')
		start = all_streaks[0]
		return start.calendar_date

	def get_streak_start_date_cohort(self, streak):
		streak_index = streak.streak_index
		user = streak.user
		all_streaks = self.md_Streak.objects.filter(user=user, streak_index=streak_index).order_by('calendar_date')
		start = all_streaks[0]
		return start.cohort_day

	def generate_survey(self, section_type):
		generated_survey = []
		#wrong
		survey = self.md_Question.objects.filter(section=section_type)
		for question in survey:
			if not question.category=="mcq":
				generated_survey.append({'index': 0, 'type': question.category, 'question': question.content, 'isAnswered': False, 'answer':""})
			else:
				generated_options = []
				options = self.md_Option.objects.filter(question=question)
				for option in options:
					generated_options.append(option.content)
				generated_survey.append({'index': 0, 'type': question.category, 'question': question.content, 'isAnswered': False, 'answer':"", 'options':generated_options})

	def fetch_all_steps(self, user, start_date, end_date):
		day = self.dt_datetime.timedelta(days=1)
		single_date = start_date
		step_list = []
		while single_date <= end_date:
			stepcount = self.md_Stepcount.objects.get(user=user, date=single_date).step_count
			step_list.append(stepcount)
			single_date = single_date + day
		return step_list

	def fetch_all_dates(self, start_date, end_date):
		day = self.dt_datetime.timedelta(days=1)
		single_date = start_date
		date_list = []
		while single_date <= end_date:
			date_list.append(single_date.isoformat())
			single_date = single_date + day
		return date_list

	def generate_section_streak_comparison(self, streak, comparison_target, awareness):
		generated_survey = self.generate_survey("streak_comparison")
		
		streak_cluster_id = streak.streak_cluster_id
		streak_info = self.md_Streakinfo.objects.get(id=streak_cluster_id)
		streak_group_info = streak_info.group
		streak_group_name = streak_group_info.name
		streak_group_description = streak_group_info.description
		streak_extra_description = streak_info.description

		recommend_streak_group_id = streak_group_info.recommendation_id_ongoing #to check status!!
		recommend_streak_group_info = self.md_Streakgroupinfo.objects.get(id=recommend_streak_group_id)
		recommend_streak_group_name = recommend_streak_group_info.name
		recommend_streak_group_description = recommend_streak_group_info.description

		user_cluster_id = streak.user_cluster_id
		user_cluster_info = self.md_Userclusterinfo.objects.get(id=user_cluster_id) #yet to do in db
		user_cluster_group_info = user_cluster_info.group
		user_cluster_group_id = user_cluster_group_info.id
		user_cluster_group_name = user_cluster_group_info.name

		start_date = self.get_streak_start_date(streak)
		end_date = streak.calendar_date

		cohort_start_date = self.get_streak_start_date_cohort(streak)
		cohort_end_date = streak.cohort_day

		calendar_steps = []
		cohort_steps = []

		user = streak.user
		all_steps = self.fetch_all_steps(user, start_date, end_date)
		all_dates = self.fetch_all_dates(start_date, end_date)

		calendar_steps = self.generate_comparison_calendar(recommend_streak_group_id, user_cluster_group_id, start_date, end_date, comparison_target, awareness)
		cohort_steps = self.generate_comparison_cohort(recommend_streak_group_id, user_cluster_group_id, cohort_start_date, cohort_end_date, comparison_target, awareness)

		return {
					'type' : "streak-comparison",
					'hasFinishedSurvey' : False,
					'comparisonTaraget' : comparison_target, #or all
					'streakName' : streak_group_name,
					'streakDescription' : streak_group_description + streak_extra_description,
					'recommendStreakName' : recommend_streak_group_name,
					'recommendStreakDescription' : recommend_streak_group_description,
					'userClusterName' : user_cluster_group_name,
					'startDate' : start_date.isoformat(),
					'endDate' : end_date.isoformat(),
					'steps' : all_steps,
					'dates': all_dates,
					'calendarSteps' : calendar_steps,
					'cohortSteps' : cohort_steps,
					'survey' : generated_survey
				}

	def generate_section_stats_comparison(self, streak, comparison_target, awareness):
		generated_survey = self.generate_survey("stats_comparison")

		user_cluster_id = streak.user_cluster_id
		user_cluster_info = self.md_Userclusterinfo.objects.get(id=user_cluster_id) #yet to do in db
		user_cluster_group_info = user_cluster_info.group
		user_cluster_group_name = user_cluster_group_info.name

		end_date = streak.calendar_date
		start_date = end_date - datetime.timedelta(days=7)

		if comparison_target == "all":
			calendar_steps = generate_comparison_all_calendar(streak)
			cohort_steps = generate_comparison_all_cohort(streak)
		elif comparison_target == "group":
			calendar_steps = generate_comparison_group_calendar(streak)
			cohort_steps = generate_comparison_group_cohort(streak)

		return {
					'type' : "stats-comparison",
					'hasFinishedSurvey' : False,
					'comparisonTarget' : comparison_target,
					'userClusterName' : user_cluster_group_name,
					'startDate' : start_date,
					'endDate' : end_date,
					'survey' : generated_survey
				}

	#todo: check control grp to pick the right comparison
	def generate_section_comparison(self, streak, comparison_target, awareness):
		section_streak_comparison = self.generate_section_streak_comparison(streak, comparison_target, awareness)
		#section_stats_comparison = self.generate_section_stats_comparison(streak, comparison_target, awareness)
		return section_streak_comparison

	def generate_section_prev_challenge(self):
		generated_survey = []
		#wrong
		survey = self.md_Question.objects.filter(section="challenge_completed")
		for question in survey:
			if not question.category=="mcq":
				generated_survey.append({'index': 0, 'type': question.category, 'question': question.content, 'isAnswered': False, 'answer':""})
			else:
				generated_options = []
				options = self.md_Option.objects.filter(question=question)
				for option in options:
					generated_options.append(option.content)
				generated_survey.append({'index': 0, 'type': question.category, 'question': question.content, 'isAnswered': False, 'answer':"", 'options':generated_options})
		
		return {
					'type' : "challenge-prev",
					'hasFinishedSurvey' : False,
					'hasPicked' : True,
					'hasCompleted' : False,
					'hasGivenup' : False,
					'hasAttempted' : False,
					'content' : {
						'title': "Stay active for 30 min when watching TV.",
						'category': "leisure",
						'content' : "Go for a 10 min walk today",
						'fun' : 5,
						'difficulty' : 2
					},
					'survey' : generated_survey
					}

	def generate_section_challenge(self):
		return {
					'type' : "challenge",
					'hasFinishedSurvey' : False,
					'hasPicked' : False,
					'pickedIdx' : 0,
					'hasCompleted' : False,
					'hasGivenup' : False,
					'hasAttempted' : False,
					'options' : [
					{
						'title': "Stay active for 30 min when watching TV.",
						'content' : "Go for a 10 min walk today",
						'fun' : 5,
						'difficulty' : 2,
						'duration': "30min"
					}, {
						'title': "Try listening to an audiobook when walking.",
						'content' : "Listen to 5 songs and run",
						'fun' : 5,
						'difficulty' : 3,
						'duration' : "20min"
					}, {
						'title': "Walk 1000 steps more when you are coming back home.",
						'content' : "Contact your best friend and go for a short walk together!",
						'fun' : 4,
						'difficulty' : 2,
						'duration' : "20min"
					}],
					'pre_survey' : [{
						'index' : 0,
						'type' : "likert",
						'question' : "To what extent do you feel inferior after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}, {
						'index' : 1,
						'type' : "likert",
						'question' : "To what extent do you feel encouraged after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}],
					'complete_survey' : [{
						'index' : 0,
						'type' : "likert",
						'question' : "To what extent do you feel inferior after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}, {
						'index' : 1,
						'type' : "likert",
						'question' : "To what extent do you feel encouraged after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}],
					'attempted_survey' : [{
						'index' : 0,
						'type' : "likert",
						'question' : "To what extent do you feel inferior after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}, {
						'index' : 1,
						'type' : "likert",
						'question' : "To what extent do you feel encouraged after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}],
					'unattempted_survey' : [{
						'index' : 0,
						'type' : "likert",
						'question' : "To what extent do you feel inferior after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}, {
						'index' : 1,
						'type' : "likert",
						'question' : "To what extent do you feel encouraged after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}]
					}

	def send_messages(self):
		# store_latest_steps
		ref = self.fb_db.reference('profile')
		userList = ref.get()
		# database
		for key, val in userList.items():
			msgref = self.fb_db.reference('profile/'+key+'/messages')
			print("inside a user")
			#section_graph = self.generate_section_graph()
			streak = self.md_Streak.objects.get(user_id="8", calendar_date=self.dt_date(2015,11,22).isoformat()) #122
			section_comparison = self.generate_section_comparison(streak, "group", "streak")
			section_challenge = self.generate_section_challenge()
			#section_prev_challenge = self.generate_section_prev_challenge()
			
			new_msg_ref = msgref.push()
			new_msg_ref.set({
				'content': "hehahah",
				'time': {'date': 8, 'month': 4, 'year': 2018},
				'hasCompleted': False,
				'sections': [section_comparison, section_challenge]
			})



	#generate msg and store it to firebase
	#message, created = Message.objects.update_or_create(
		#date=date.today(), defaults={'user_id': key, 'message_id': key})
	#print stepcount
	
ms = MessageSender(db, Q, Question, Option, Stepcount, Streak, StreakInfo, StreakGroupInfo, UserClusterInfo, UserClusterGroupInfo, date, datetime, math)
ms.send_messages()

start_date = date.today()
#print(ms.generate_comparison_all_calendar(4, start_date-datetime.timedelta(1), start_date))


