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


# store_latest_steps
ref = db.reference('profile')
userList = ref.get()

insert_list = {}

for key, val in userList.items():
	user, created = User.objects.update_or_create(
		user_id=key, defaults={'comparison': 'fd', 'context': 'sl'}
		)
	insert_list[key] = val['steps']
	for key2 in val['steps']:
		stepcount=val['steps'][key2]
		user=User.objects.get(user_id=key)
		stepcount, created = Stepcount.objects.update_or_create(
			date=date(stepcount['year'], stepcount['month'], stepcount['date']), defaults={'user_id': user, 'step_count': stepcount['step']})
		print stepcount
	print "yohoo"

		#ref2 = db.reference('profile/{key}/steps')
		#snapshot = ref2.order_by_child().limit_to_first(7).get()
	#print stepKey
		#stepcount, created = Stepcount.objects.update_or_create(
			#date=date(stepVal['year'], stepVal['month'], stepVal['date']), defaults={'user_id': key}
			#)
	#user = User(user_id=key, comparison='all', context='semantic')
	#user.save()
	#print '{0} and {1}' .format(key, val['steps'])
	#print "hehehe"

#for key in insert_list:
#	val=insert_list[key]
#	print val
#	for key2, stepVal in val:
		#stepcount, created = Stepcount.objects.update_or_create(
				#date=datetime.date(stepVal['year'], stepVal['month'], stepVal['date']), defaults={'user_id': key2}
				#)
		