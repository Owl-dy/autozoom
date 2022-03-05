import csv, os, time, datetime
from utils import *

if __name__ == '__main__':

	##processing the csv and create a meeting list
	meeting_list = []
	file_path = os.path.abspath(os.path.dirname(__file__))
	csv_path = os.path.join(file_path, 'schedule.csv')

	with open(csv_path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
			else:
				line_count += 1
				meeting = Meeting(row[0],row[1], row[2], row[3], row[4])
				meeting_list.append(meeting)

		print(f'Processed {line_count - 1} meetings.')

	#sorting meeting list
	meeting_list = sorted(meeting_list, key = lambda x : x.start_time)


	# loop_count = 0 for debugging

	while len(meeting_list) > 0:

		# loop_count += 1

		# if the first meeting on the list (aka, the current meeting) is not yet started, wait
		if datetime.datetime.now() < meeting_list[0].start_time + datetime.timedelta(minutes=LATE_THRESHOLD):
			while datetime.datetime.now() < meeting_list[0].start_time:
				# checking in interval until the meeting.start_time has past
				print(
					f'currently is {datetime.datetime.now()}, and the next meeting is in {(meeting_list[0].start_time - datetime.datetime.now()).total_seconds() / 60} mins')
				time.sleep(LATE_THRESHOLD * 60)
			print(
				f'currently is {datetime.datetime.now()}, joining the meeting that starts at {meeting_list[0].start_time}......')
			meeting_list[0].join()
			time.sleep(10)

		# if the current meeting is not yet over, sleep until the meeting ends
		meeting_remaining_time = (meeting_list[0].end_time - datetime.datetime.now()).total_seconds()
		if meeting_remaining_time > 0:
			print(f'currently is {datetime.datetime.now()}, in session, and the meeting ends at {meeting_list[0].end_time}')
			time.sleep(meeting_remaining_time)

		# if the current time is after the ending time of the current meeting, exiting zoom and popping the meeting off the meeting list
		if datetime.datetime.now() > meeting_list[0].end_time:
			print(f'exiting meeting that ends at {meeting_list[0].end_time}')
			meeting_list[0].quit()
			time.sleep(10) # pause for app to close gracefully
			meeting_list.pop(0)
			print(f'there are {len(meeting_list)} more meetings to be attended')

		else:
			print(bcolors.WARNING+ 'something wrong' + bcolors.ENDC)

	print(bcolors.OKGREEN+'program finished... see you next time'+bcolors.ENDC)
