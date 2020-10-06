import csv, time, datetime, platform
from playsound import playsound
from utils import Meeting, Windows, Mac


#consent to turn on camera and audio
consent = input(' Would you like to turn on your camera or mic for the meetings? \n Please make sure virtual background is set up on Zoom \n Please make sure your audio file is named audio_only.wav in the same directory \n Do you consent? y/[N] \n')
consent = True if consent.lower() == 'y' or consent.lower() == 'yes' else False 

LATE_THRESHOLD = 2 #mins
VIDEO_TIME = int(input('How long would you loop your video for (mins)?' )) #mins --- to loop the virtual background

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
        	meeting = Meeting(row[0],row[1],row[2],row[3],row[4],row[5])
        	meeting_list.append(meeting)
            
    print(f'Processed {line_count - 1} meetings.')


#checking for the system
op = Windows() if platform.system() == 'Windows' else Mac()



#loop for checking meetings in the list 
while len(meeting_list) > 0:
     #if the first meeting on the list (aka, the current meeting) is not yet started, wait 
	if datetime.datetime.now() < meeting_list[0].start_time :
		while datetime.datetime.now() < meeting_list[0].start_time:
			#checking in interval until the meeting.start_time has past
			print(f'currently is {datetime.datetime.now()}, and the next meeting is in {(meeting_list[0].start_time - datetime.datetime.now()).total_seconds()/60} mins')
			time.sleep(LATE_THRESHOLD * 60)
		print(f'currently is {datetime.datetime.now()}, joining the meeting that starts at {meeting_list[0].start_time}......')
		op.join(meeting_list[0])
		time.sleep(15)
		

		if consent:
			## opening up camera
			if meeting_list[0].video: 
				op.camera_action()#open camera
			
			time.sleep(2)
			## opening up audio
			if meeting_list[0].audio:
				op.audio_action()#turn on audio
				playsound('audio_only.wav') #play the audio until finished
				op.audio_action()#mute 
			
			time.sleep(VIDEO_TIME*60)#keep camera open 
			op.camera_action()#off camera



 	#if the current meeting is not yet over, sleep until the meeting ends
	meeting_remaining_time = (meeting_list[0].end_time - datetime.datetime.now()).total_seconds()
	if meeting_remaining_time > 0:	
		print(f'currently is {datetime.datetime.now()}, in session, and the meeting ends at {meeting_list[0].end_time}')
		time.sleep(meeting_remaining_time)


	#if the current time is after the ending time of the current meeting, exiting zoom and popping the meeting of the meeting list	
	if datetime.datetime.now() > meeting_list[0].end_time:
		print(f'exiting meeting that ends at {meeting_list[0].end_time}')
		op.quit()
		time.sleep(10)
		meeting_list.pop(0)
		print(f'there are {len(meeting_list)} more meetings to be attended')

	else:
		print('something wrong')

print('program finished... see you next time')






