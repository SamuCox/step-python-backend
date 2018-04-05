import firebase_admin
from firebase_admin import credentials, db
from django.db.models import Max
from stepserver.models import User, Stepcount, Streak
from datetime import date
import datetime
from django.core.exceptions import ObjectDoesNotExist

# Fetch the service account key JSON file contents
cred = credentials.Certificate('service-account-key.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://step-customer.firebaseio.com/'
	})

# As an admin, the app has access to read and write all data, regradless of Security Rules
# ref = db.reference('restricted_access/secret_document')
# print ref.get()
class StepStorageManager:

	def __init__(self, db_Max, fb_db, dt_date, dt_datetime, md_User, md_Stepcount, md_Streak, ex_ObjectDoesNotExist):
		self.fb_db = fb_db
		self.db_Max = db_Max
		self.md_User = md_User
		self.md_Stepcount = md_Stepcount
		self.md_Streak = md_Streak
		self.dt_date = dt_date
		self.dt_datetime = dt_datetime
		self.ex_ObjectDoesNotExist = ex_ObjectDoesNotExist

	def store_all_users_and_steps(self):
		ref = self.fb_db.reference('profile')
		userList = ref.get()
		user = None

		insert_list = {}

		for key, val in userList.items():
			print("try this!")
			#need to check whether the user is new or not. If yes, give him/her a start date.
			self.check_and_add_user(key)
			insert_list[key] = val['steps']

			for key2 in val['steps']:
				stepcount=val['steps'][key2]
				user=self.md_User.objects.get(user_id=key)
				stepcount, created = self.md_Stepcount.objects.update_or_create(
					date=self.dt_date(stepcount['year'], stepcount['month'], stepcount['date']), user=user, defaults={'step_count': stepcount['step']})
				print stepcount
				print "yohoo"
			# make up a 0 record if the user does not record his/her data today
			current_date = self.dt_date.today()
			user = self.md_User.objects.get(user_id=key)
			self.check_and_add_step(user, current_date)
			self.store_current_cluster(user)

	def check_and_add_user(self, user_id):
		try:
			user = self.md_User.objects.get(user_id=user_id)
		except self.ex_ObjectDoesNotExist:
			current_date = self.dt_date.today()
			user = self.md_User(user_id=user_id, comparison='all', context='yes', start_date=current_date)
			user.save()

	def check_and_add_step(self, user, current_date):
		try:
			today_stepcount = self.md_Stepcount.objects.get(user=user, date=current_date)
		except self.ex_ObjectDoesNotExist:
			today_stepcount = self.md_Stepcount(user=user, date=current_date, step_count=0)
			today_stepcount.save()

	def get_streak_cluster_id_temp(self):
		return 4

	def get_streak_cluster_id(self, streak_list):
		return 4

	def get_user_cluster_id(self):
		return 4

	def store_current_cluster(self, user):
		start_date = user.start_date
		# take out the current streak cluster
		has_encountered_active = False
		has_encountered_inactive = False
		is_today_active = False
		is_first_streak_start = False
		is_streak_start = False
		current_date = self.dt_date.today()
		today_date = self.dt_date.today()
		step_count = self.md_Stepcount.objects.get(user=user, date=current_date)

		current_streak_index = 0
		active_level = 50

		if step_count.step_count > active_level:
			is_today_active = True
			has_encountered_active = True
			#check whether this is the start of the first streak
			try:
				streak = self.md_Streak.objects.get(user=user)
			except self.ex_ObjectDoesNotExist:
				is_first_streak_start = True
		
		streak_list = []
		while (not has_encountered_inactive) and (current_date >= start_date):
			print(current_date)
			try:
				step_count = self.md_Stepcount.objects.get(user=user, date=current_date)
				count = step_count.step_count
				if count > active_level:
					has_encountered_active = True
					current_date = current_date - self.dt_datetime.timedelta(1)
					streak_list.append(count)
				else:
					# if already encountered active and then encounter inactive now, end the streak
					if has_encountered_active:
						has_encountered_inactive = True
					else:
						streak_list.append(0)
					if current_date == start_date:
						current_date = current_date - self.dt_datetime.timedelta(1)
			except self.ex_ObjectDoesNotExist:
				streak, created = self.md_Stepcount.objects.update_or_create(
					user=user, date=current_date, defaults={'step_count': 0})
    		if has_encountered_active:
    			has_encountered_inactive = True
    		else:
					current_date = current_date - self.dt_datetime.timedelta(1)
					streak_list.append(0)

		streak_start_date = current_date + self.dt_datetime.timedelta(1)
		streak_list.reverse()
		streak_cluster_id = self.get_streak_cluster_id(streak_list)

		#get previous result of cluster id, +1 if this is a new streak
		if streak_list.count == 1:
			is_streak_start = True
		
		if has_encountered_active:
			if not is_first_streak_start:
				latest_streak_record = self.md_Streak.objects.all().aggregate(self.db_Max('cohort_end_date'))['cohort_end_date__max']
				prev_cluster_id = self.md_Streak.objects.get(user=user, cohort_end_date = latest_streak_record).streak_id

			if is_first_streak_start:
				current_streak_index = 0
			elif is_streak_start:
				current_streak_index = prev_cluster_id + 1
			else:
				current_streak_index = prev_cluster_id

			cohort_start_date = (streak_start_date - start_date).days
			cohort_end_date = (today_date - start_date).days

			#save streak to dbstreak_start_date
			streak, created = self.md_Streak.objects.update_or_create(
						user=user, end_date=today_date, defaults={'streak_id': streak_cluster_id, 'streak_index': current_streak_index, 'start_date': streak_start_date, 'cohort_start_date': cohort_start_date, 'cohort_end_date': cohort_end_date, 'is_active': is_today_active})




ms = StepStorageManager(Max, db, date, datetime, User, Stepcount, Streak, ObjectDoesNotExist)
ms.store_all_users_and_steps()