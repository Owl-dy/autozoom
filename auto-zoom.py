import csv, os, time, datetime

# max runtime of the auto-zoom program (in hours)
MAX_TIME = 24

# max time allowed to be late for a meeting (in mins)
LATE_THREHOLD = 15

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

while len(meeting_list) != 0:

	#if the current time is after the ending time, exiting zoom and popping the meeting of the meeting list	
	if datetime.datetime.now() > meeting_list[0].end_time:
		print(f'exiting meeting that ends at {meeting_list[0].end_time}')
		os.system('killall zoom.us')
		time.sleep(10)
		meeting_list.pop(0)

     #if the first meeting on the list is not yet started, wait till then and join
	time_to_next_meeting = (meeting_list[0].start_time - datetime.datetime.now()).total_seconds() 
	if time_to_next_meeting > 0 :
		print(f'currently is {datetime.datetime.now()}, and the next meeting is in {time_to_next_meeting/60} mins, see you then')
		time.sleep(time_to_next_meeting)
		meeting_list[0].join()
		time.sleep(10)   


 	#if the current meeting is not yet over, sleep until the meeting ends
	meeting_remaining_time = (meeting_list[0].end_time - datetime.datetime.now()).total_seconds()
	if meeting_remaining_time > 0:	
		print(f'currently is {datetime.datetime.now()}, in session, and the meeting ends at {meeting_list[0].end_time}')
		time.sleep(meeting_remaining_time)



	else:
		print(f'there are {len(meeting_list)} more meetings to be attended')








