import csv
from stepserver.models import Stepcount, Streak, User

def import_data(csv, User, Stepcount, Streak):
	path = 'fixtures/external_data.csv'
	with open(path) as f:
		reader = csv.reader(f)
		next(reader)
		for row in reader:
			user, created = User.objects.update_or_create(
					user_id=row[0])
			user = User.objects.get(user_id=row[0])
			stepcount, created = Stepcount.objects.update_or_create(
					user=user, date=row[6], defaults={'step_count': row[13]})
			streak, created = Streak.objects.update_or_create(
					user=user, calendar_date=row[6], defaults={'streak_index': row[1], 'streak_cluster_id': row[7], 'user_cluster_id': row[11], 'cohort_day': row[4], 'step_count': row[13]})
 
import_data(csv, User, Stepcount, Streak);