import firebase_admin
from firebase_admin import credentials, db
from stepserver.models import User, Stepcount, Streak, Max
from datetime import date, datetime
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

	def __init__(self, fb_db, dt_date, dt_datetime, md_User, md_Stepcount, md_Streak):
		self.fb_db = fb_db
		self.md_User = md_User
		self.md_Stepcount = md_Stepcount
		self.md_Streak = md_Streak
		self.dt_date = dt_date
		self.dt_datetime = dt_datetime

	def store_all_users_and_steps(self):
		# store_latest_steps
		ref = self.fb_db.reference('profile')
		userList = ref.get()

		insert_list = {}

		for key, val in userList.items():
			#need to check whether the user is new or not. If yes, give him/her a start date.
			try:
    		user = self.md_User.objects.get(user_id=key)
			except ObjectDoesNotExist:
				current_date = self.dt_date.today()
    		user = self.md_User(user_id=key, comparison='all', context='yes', start_date=current_date)
    		today_stepcount.save()

			insert_list[key] = val['steps']
			for key2 in val['steps']:
				stepcount=val['steps'][key2]
				user=self.md_User.objects.get(user_id=key)
				stepcount, created = self.md_Stepcount.objects.update_or_create(
					date=self.dt_date(stepcount['year'], stepcount['month'], stepcount['date']), defaults={'user': user, 'step_count': stepcount['step']})
				print stepcount
				print "yohoo"
			# make up a 0 record if the user does not record his/her data today
			current_date = self.dt_date.today()
			user = self.md_User.objects.get(user_id=key)
			try:
    		today_stepcount = self.md_Stepcount.objects.get(user=user, date=current_date)
			except ObjectDoesNotExist:
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

		if step_count.step_count > 500:
			is_today_active = True
			has_encountered_active = True
			#check whether this is the start of the first streak
			try:
				streak = self.md_Streak.objects.get(user=user)
			except ObjectDoesNotExist:
				is_first_streak_start = True
		
		streak_list = []
		while !has_encountered_inactive && current_date >= start_date:
			try:
				step_count = self.md_Stepcount.objects.get(user=user, date=current_date)
				count = step_count.step_count
				if count > 500:
					has_encountered_active = True
					current_date = current_date - self.dt_datetime.timedelta(1)
					streak_list.append(count)
				else:
					# if already encountered active and then encounter inactive now, end the streak
					if has_encountered_active:
						has_encountered_inactive = True
			except ObjectDoesNotExist:
				makeup_stepcount = self.md_Stepcount(user=user, date=current_date, step_count=0)
    		makeup_stepcount.save()
				if has_encountered_active:
					# mark as end
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
		
		if !is_first_streak_start:
			latest_streak_record = md_Streak.objects.all().aggregate(Max('cohort_end_date'))['cohort_end_date__max']
			prev_cluster_id = md_Streak.objects.get(cohort_end_date = latest_streak_record).streak_id

		if is_first_streak_start:
			current_streak_index = 0
		elif is_streak_start:
			current_streak_index = prev_cluster_id + 1
		else:
			current_streak_index = prev_cluster_id

		cohort_start_date = streak_start_date - start_date
		cohort_end_date = today_date - start_date

		#save streak to dbstreak_start_date
		#todo: change to update/add
		latest_streak = self.md_Streak(user=user, streak_id=streak_cluster_id, streak_index=current_streak_index, start_date=streak_start_date, end_date=today_date, cohort_start_date=cohort_start_date, cohort_end_date=cohort_end_date, is_active=is_today_active)
    latest_streak.save()




ms = StepStorageManager(db, date, datetime, User, Stepcount, Streak)
ms.store_all_users_and_steps()