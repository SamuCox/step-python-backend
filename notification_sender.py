import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate('service-account-key.json')
default_app = firebase_admin.initialize_app(cred)


def sendNotification(fb_messaging):
	# The topic name can be optionally prefixed with "/topics/".
	topic = 'all'

	# See documentation on defining a message payload.
	message = fb_messaging.Message(
		notification=fb_messaging.Notification(
			title="pythonYooooo",
			body="Notification body"
			)  ,
		topic=topic,
		)

	# Send a message to the devices subscribed to the provided topic.
	response = fb_messaging.send(message)
	# Response is a message ID string.
	print('Successfully sent message:', response)

sendNotification(messaging);