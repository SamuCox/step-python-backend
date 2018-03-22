import firebase_admin
from firebase_admin import credentials, db
from stepserver.models import User, Message
from datetime import date

# Fetch the service account key JSON file contents
cred = credentials.Certificate('service-account-key.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://step-customer.firebaseio.com/'
	})

# store_latest_steps
ref = db.reference('profile')
userList = ref.get()

# database
for key, val in userList.items():
	msgref = db.reference('profile/{key}/messages')
	#generate msg and store it to firebase
	message, created = Message.objects.update_or_create(
		date=date.today(), defaults={'user_id': key, 'message_id': key})
	print stepcount

def generateMsg():
