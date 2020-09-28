import csv, os, time, datetime

#how many minutes can be late for
LATE_THRESHOLD = 5

# how often to check for meeting time (in minutes)
DOWNTIME = 5

# max runtime of the auto-zoom program (in hours)
MAX_TIME = 24

def decode_link(link):
	#extract meeting info from zoom url
	password = link.split('pwd=')[1]
	conference_code = link.split('/j/')[1].split('?pwd=')[0]
	return password, conference_code

def convert_time(string):
	#converting HH:MM string to a datetime object
	hour = string.split(":")[0]
	minute = string.split(":")[1]
	# mm/dd/y hour:minute
	# to be changed if incorporating multiple days of meetings
	datetime_str = f'{datetime.date.today().strftime("%m/%d/%y")} {hour}:{minute}:00'
	datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
	return datetime_object

class Meeting():
	#a meeting is consisted of the meeting link and the meeting time
	def __init__(self, link, start_time, end_time):
		self.start_time = convert_time(start_time)
		self.end_time = convert_time(end_time)
		self.password, self.conference_code = decode_link(link)

	def join(self):
	#using terminal to open converted zoom link
		command = f'open "zoommtg://zoom.us/join?confno={self.conference_code}?&pwd={self.password}"'
		os.system(command)





##processing the csv and create a meeting list
meeting_list = []

with open('schedule.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
        	line_count += 1
        	meeting = Meeting(row[0],row[1],row[2])
        	meeting_list.append(meeting)
            
    print(f'Processed {line_count - 1} meetings.')

 


start_time = time.time()

while time.time() - start_time < MAX_TIME * 60 * 60:
	#if the program run time is less than 8 hours, continue to check for meetings

	time_since_meeting_started = (datetime.datetime.now() - meeting_list[0].start_time).total_seconds() 

	if datetime.datetime.now() > meeting_list[0].end_time:
		#if the current time is the ending time, quitting the meeting
		print('exiting meeting')
		os.system('killall zoom.us')
		meeting_list.pop(0)		

	elif time_since_meeting_started < LATE_THRESHOLD * 60 and time_since_meeting_started > 0 :
		#if the current time is the meeting time and not deemed late, join the meeting
		print('joining')
		meeting_list[0].join()
		#stay on for at least 10mins
		time.sleep(600)

	else:	
		#wait to check in 1 min
		print(f'currently is {datetime.datetime.now()}, and the next meeting is {meeting_list[0].start_time}')
		time.sleep(DOWNTIME * 60)


