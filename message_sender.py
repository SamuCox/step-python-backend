import firebase_admin
from firebase_admin import credentials, db
from stepserver.models import Question, Option
from datetime import date

# Fetch the service account key JSON file contents
cred = credentials.Certificate('service-account-key.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://step-customer.firebaseio.com/'
	})

class MessageSender:

	def __init__(self, fb_db, md_Question, md_Option):
		self.fb_db = fb_db

	#take in uid, steps(?), date
	#require control grp info
	#graph: need no. of dates, content -> [need ctrl-grp to decide how many days to show & content (if streak): pull out the last/current streak; if not, show last WEEK]
	def generate_message(self):
		print()

	def generate_section_streak_graph(self):
		#user=md_User.objects.get(user_id=key)
		streakGraphPreQuestions = md_Question.objects.filter(section='streak_graph_pre')
		streakGraphPostQuestions = md_Question.objects.filter(section='streak_graph_post')
		return {
					'type' : "graph",
					'startTime' : "2018-02-08",
					'endTime' : "2018-02-15",
					'steps': [8201, 7500, 9020, 7502, 6702, 9520, 8640],
					'dates': [8, 9, 10, 11, 12, 13, 14, 15],
					'content' : "You walk a lot"
				}

	def generate_section_stats_graph(self): 
	 
	def generate_section_graph(self):  

	def generate_section_streak_comparison(self):
		return {
					'type' : "streak-comparison",
					'target' : "all",
					'streakID' : 12,
					'recommendID' : 15,
					'percentile' : 75,
					'startTime' : "2018-02-11",
					'endTime' : "2018-02-15",
					'steps' : [7502, 6702, 9520, 8640, 10020],
					'dates': [11, 12, 13, 14, 15],
					'streakDescription' : "You are walking slowly",
					'recommendDescription' : "Try walking faster",
					'survey' : [{
						'index' : "0",
						'type' : "field",
						'question' : "How do you feel when looking at the comparison?",
						'isAnswered' : False,
						'answer' : ""
					}, {
						'index' : "0",
						'type' : "likert",
						'question' : "To what extent do you feel inferior after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}, {
						'index' : "1",
						'type' : "likert",
						'question' : "To what extent do you feel encouraged after seeing comparisons to other users?",
						'isAnswered' : False,
						'answer' : ""
					}, {
						'index' : "0",
						'type' : "mcq",
						'question' : "Why didn’t you complete the challenge?",
						'options' : ["I don't like it", "I am too tired"],
						'isAnswered' : False,
						'answer' : ""
					}]
				}
	
	def generate_section_stats_comparison(self):
		return {
					'type' : "stats-comparison",
					'steps' : 7420,
					'percentile' : 60,
					'recommendPercentile' : 80,
					'recommendSteps' : 8920,
					'statsDescription' : "You are walking too few",
					'survey' : [{
						'index' : 0,
						'type' : "field",
						'question' : "How do you feel when looking at the comparison?",
						'isAnswered' : False,
						'answer' : ""
					}, {
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
					}, {
						'index' : 0,
						'type' : "mcq",
						'question' : "Why didn’t you complete the challenge?",
						'options' : ["I don't like it", "I am too tired"],
						'isAnswered' : False,
						'answer' : ""
					}]
				}

	#todo: check control grp to pick the right comparison
	def generate_section_comparison():
		section_streak_comparison = self.generate_section_streak_comparison()
		section_stats_comparison = self.generate_section_stats_comparison()
		return section_streak_comparison

	def generate_section_challenge():
		return {
					'type' : "challenge",
					'hasPicked' : False,
					'pickedIdx' : 0,
					'hasCompleted' : False,
					'options' : [
					{
						'title': "Walk 10 min",
						'category': "leisure",
						'content' : "Go for a 10 min walk today",
						'fun' : 5,
						'difficulty' : 2
					}, {
						'title': "Listen to music and run",
						'category': "leisure",
						'content' : "Listen to 5 songs and run",
						'fun' : 5,
						'difficulty' : 3
					}, {
						'title': "Find a friend to walk",
						'category': "Social",
						'content' : "Contact your best friend and go for a short walk together!",
						'fun' : 4,
						'difficulty' : 2
					}

	def send_messages(self):
		# store_latest_steps
		ref = self.fb_db.reference('profile')
		userList = ref.get()
		# database
		for key, val in userList.items():
			msgref = self.fb_db.reference('profile/'+key+'/messages')
			print("inside a user")
			section_graph = self.generate_section_graph()
			section_comparison = self.generate_section_comparison()
			section_challenge = self.generate_section_challenge()
			
			new_msg_ref = msgref.push()
			new_msg_ref.set({
				'content': "hehahah",
				'time': {'date': 15, 'month': 2, 'year': 2018},
				'hasCompleted': False,
				'sections': [section_graph, section_comparison, section_challenge]
			})


	#generate msg and store it to firebase
	#message, created = Message.objects.update_or_create(
		#date=date.today(), defaults={'user_id': key, 'message_id': key})
	#print stepcount
	
ms = MessageSender(db, Question, Option)
ms.send_messages()