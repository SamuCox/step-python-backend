import firebase_admin
from firebase_admin import credentials, db
from stepserver.models import User, Stepcount
from datetime import date

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

	def __init__(self, fb_db, dt_date, md_User, md_Stepcount):
		self.fb_db = fb_db
		self.md_User = md_User
		self.md_Stepcount = md_Stepcount
		self.dt_date = dt_date

	def store_all_users_and_steps(self):
		# store_latest_steps
		ref = self.fb_db.reference('profile')
		userList = ref.get()

		insert_list = {}

		for key, val in userList.items():
			user, created = self.md_User.objects.update_or_create(
				user_id=key, defaults={'comparison': 'fd', 'context': 'sl'}
				)
			insert_list[key] = val['steps']
			for key2 in val['steps']:
				stepcount=val['steps'][key2]
				user=self.md_User.objects.get(user_id=key)
				stepcount, created = self.md_Stepcount.objects.update_or_create(
					date=self.dt_date(stepcount['year'], stepcount['month'], stepcount['date']), defaults={'user': user, 'step_count': stepcount['step']})
				print stepcount
				print "yohoo"

ms = StepStorageManager(db, date, User, Stepcount)
ms.store_all_users_and_steps()