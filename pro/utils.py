from pynput.keyboard import Key, Controller
import datetime, os, time


def decode_link(link):
	#extract meeting info from zoom url
	password = link.split('pwd=')[1]
	conference_code = link.split('/j/')[1].split('?pwd=')[0]
	return password, conference_code

def convert_time(string_date, string_time):
	#converting HH:MM string to a datetime object
	hour = string_time.split(":")[0]
	minute = string_time.split(":")[1]

	# mm/dd/y hour:minute
	if string_date == '':
		#leave blank for today
		datetime_str = f'{datetime.date.today().strftime("%m/%d/%y")} {hour}:{minute}:00'
	else:
		datetime_str = f'{string_date} {hour}:{minute}:00'
	datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')


	return datetime_object



class Meeting():
	#a meeting is consisted of the meeting link and the meeting time
	def __init__(self, link, date, start_time, end_time, video, audio):
		self.start_time = convert_time(date, start_time)
		self.end_time = convert_time(date, end_time)
		self.password, self.conference_code = decode_link(link)
		video = video.strip()# getting rid of space issues
		audio = audio.strip()
		self.video = True if video.lower() == 'y' or video.lower() == 'yes' else False
		self.audio = True if audio.lower() == 'y' or audio.lower() == 'yes' else False



class Windows():

	def __init__(self):
		self.keyboard = Controller()
		return None

	def join(self, meeting):
		command = f'start zoommtg://zoom.us/join?confno={meeting.conference_code}?"&"pwd={meeting.password}'
		os.system(command)

	def quit(self):
		os.system('taskkill /f /im Zoom.exe')

	def camera_action(self):
		self.keyboard.press(Key.alt_l)
		time.sleep(1)
		self.keyboard.press('v')
		time.sleep(1)
		self.keyboard.release('v')
		time.sleep(1)
		self.keyboard.release(Key.alt_l)

	def audio_action(self):
		self.keyboard.press(Key.alt_l)
		self.keyboard.press('a')
		time.sleep(1)
		self.keyboard.release('a')
		self.keyboard.release(Key.alt_l)





class Mac():

	def __init__(self):
		self.keyboard = Controller()
		return None

	def join(self, meeting):
		command = f'open "zoommtg://zoom.us/join?confno={meeting.conference_code}?&pwd={meeting.password}"'
		os.system(command)

	def quit(self):
		os.system('killall zoom.us')

	def camera_action(self):
		self.keyboard.press(Key.cmd)
		self.keyboard.press(Key.shift)
		time.sleep(1)
		self.keyboard.press('v')
		time.sleep(1)
		self.keyboard.release('v')
		self.keyboard.release(Key.cmd)
		self.keyboard.release(Key.shift)

	def audio_action(self):
		self.keyboard.press(Key.cmd)
		self.keyboard.press(Key.shift)
		time.sleep(1)
		self.keyboard.press('a')
		time.sleep(1)
		self.keyboard.release('a')
		self.keyboard.release(Key.cmd)
		self.keyboard.release(Key.shift)




