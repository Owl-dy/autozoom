import csv, os, time, datetime

LATE_THRESHOLD = 2 #mins

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
loop_count = 0

while len(meeting_list) > 0:

	loop_count += 1
	print(loop_count)

     #if the first meeting on the list (aka, the current meeting) is not yet started, wait 
	if datetime.datetime.now() < meeting_list[0].start_time :
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
		os.system('killall zoom.us')
		time.sleep(10)
		meeting_list.pop(0)
		print(f'there are {len(meeting_list)} more meetings to be attended')

	else:
		print('something wrong')

print('program finished... see you next time')






