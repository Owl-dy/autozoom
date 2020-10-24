import csv, os, time, datetime, platform

LATE_THRESHOLD = 0.5 #mins

def decode_link(link):
	#extract meeting info from zoom url
	try:
		password = link.split('pwd=')[1]
	except:
		password = input(f"The password of {link} can not be detected. \nInput the password manually or press enter. \n")
	
	try:
		conference_code = link.split('/j/')[1].split('?pwd=')[0]
	except:
		conference_code = input(f"The conference code of {link} CAN NOT be detected. \nInput the conference code manually or press enter to continue anyway.\n")
		conference_code = "NOT FOUND" if conference_code == "" else conference_code.strip()
		if conference_code == "NOT FOUND":
			print(f"The conference code of {link} CAN NOT be detected \nWill try joining this meeting with the original link. \nPlease ensure your browser will open the link with Zoom Client automatically.")
		else:
			print(f"your conference code is {conference_code}")
	return password, conference_code

def convert_time(string_date, string_time):
	#converting HH:MM string to a datetime object
	hour = string_time.split(":")[0]
	minute = string_time.split(":")[1]

	#checking for default date
	if string_date == '':
		string_date = 'today'

	# mm/dd/y hour:minute
	if string_date == 'today':
		datetime_str = f'{datetime.date.today().strftime("%m/%d/%y")} {hour}:{minute}:00'
	else:
		datetime_str = f'{string_date} {hour}:{minute}:00'
	datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
	return datetime_object

class Meeting():
	#a meeting is consisted of the meeting link and the meeting time
	def __init__(self, link, date, start_time, end_time):
		self.start_time = convert_time(date, start_time)
		self.end_time = convert_time(date, end_time)
		self.password, self.conference_code = decode_link(link)
		self.link = link

	def join(self):
		if platform.system() == 'Windows':
			if self.conference_code == "NOT FOUND":
				command = f'start {self.link}' #using the original link to join
			else:
				command = f'start zoommtg://zoom.us/join?confno={self.conference_code}?"&"pwd={self.password}'
		else: 
			if self.conference_code == "NOT FOUND":
				command = f'open {self.link}' #using the original link to join
			else:
				command = f'open "zoommtg://zoom.us/join?confno={self.conference_code}?&pwd={self.password}"'
		os.system(command)

	def quit(self):
		if platform.system() == 'Windows':
			os.system('taskkill /f /im Zoom.exe')
		else: 
			os.system('killall zoom.us')





##processing the csv and create a meeting list
meeting_list = []
file_path = os.path.abspath(os.path.dirname(__file__))
csv_path = os.path.join(file_path,'schedule.csv')

with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
        	line_count += 1
        	meeting = Meeting(row[0],row[1],row[2],row[3])
        	meeting_list.append(meeting)
            
    print(f'Processed {line_count - 1} meetings.')

 


start_time = time.time()
loop_count = 0

while len(meeting_list) > 0:

	loop_count += 1
	print(loop_count)

     #if the first meeting on the list (aka, the current meeting) is not yet started, wait 
	if datetime.datetime.now() < meeting_list[0].start_time + datetime.timedelta(minutes = LATE_THRESHOLD) :
		while datetime.datetime.now() < meeting_list[0].start_time:
			#checking in interval until the meeting.start_time has past
			print(f'currently is {datetime.datetime.now()}, and the next meeting is in {(meeting_list[0].start_time - datetime.datetime.now()).total_seconds()/60} mins')
			time.sleep(LATE_THRESHOLD * 60)
		print(f'currently is {datetime.datetime.now()}, joining the meeting that starts at {meeting_list[0].start_time}......')
		meeting_list[0].join()
		time.sleep(10)   


 	#if the current meeting is not yet over, sleep until the meeting ends
	meeting_remaining_time = (meeting_list[0].end_time - datetime.datetime.now()).total_seconds()
	if meeting_remaining_time > 0:	
		print(f'currently is {datetime.datetime.now()}, in session, and the meeting ends at {meeting_list[0].end_time}')
		time.sleep(meeting_remaining_time)


	#if the current time is after the ending time of the current meeting, exiting zoom and popping the meeting of the meeting list	
	if datetime.datetime.now() > meeting_list[0].end_time:
		print(f'exiting meeting that ends at {meeting_list[0].end_time}')
		meeting_list[0].quit()
		time.sleep(10)
		meeting_list.pop(0)
		print(f'there are {len(meeting_list)} more meetings to be attended')

	else:
		print('something wrong')

print('program finished... see you next time')






