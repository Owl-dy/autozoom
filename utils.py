import os, datetime, platform

LATE_THRESHOLD = 1 #mins

class bcolors:
	#use for showing color in terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def decode_link(link):
	""" 
	Extract and parase meeting info from zoom url
	:param: 
		link str
	:return: 
		zoom_domain_name str
		password str
		conference_code str
	"""

	try:
		password = link.split('pwd=')[1]
	except: # error catching for not including password
		print("password omitted")
		password = None

	try:
		conference_code = link.split('/j/')[1].split('?pwd=')[0]
	except: # error catching for not detecting conference code and allow for manual input
		conference_code = input(
			f"The conference code of {link} CAN NOT be detected. \nInput the conference code manually or press enter to continue anyway.\n")
		conference_code = "NOT FOUND" if conference_code == "" else conference_code.strip()
		if conference_code == "NOT FOUND":
			print(
				f"The conference code of {link} CAN NOT be detected \nWill try joining this meeting with the original link. \nPlease ensure your browser will open the link with Zoom Client automatically.")
		else:
			print(f"The conference code you entered is {conference_code}")

	try:
		zoom_domain_name = link.split("//")[1].split("/j")[0]
	except:
		zoom_domain_name = ''
		print('no domain name')

	return zoom_domain_name, password, conference_code

def convert_time(string_date, string_time):
	"""
	Converting HH:MM string to a datetime object
	:param:
		string_date str MM/DD/YYYY format
		string_time str HH:MM format
	
	"""

	# converting string_time HH:MM
	hour = string_time.split(":")[0]
	minute = string_time.split(":")[1]
	

	# converting string_date

	# check for default date
	if string_date == '':
		string_date = 'today'

	# mm/dd/y hour:minute
	if string_date == 'today':
		datetime_str = f'{datetime.date.today().strftime("%m/%d/%y")} {hour}:{minute}:00'

	# check for using day in the week
	elif string_date in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
		curdate = datetime.date.today()

		while curdate.strftime('%A') != string_date:
			curdate = curdate + datetime.timedelta(days=1)

		datetime_str = f'{curdate.strftime("%m/%d/%y")} {hour}:{minute}:00'

	# process the usual format MM/DD/YYYY
	else:
		datetime_str = f'{string_date} {hour}:{minute}:00'
	datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
	return datetime_object

def pop_up_entry(win, warning_str, with_entry = False):
	"""
	create a pop up window with warning for user to modify their meeting info
	"""
	import tkinter as tk

	#Define a function to close the popup window
	def close_win(top):
		top.destroy()

	#Create a Toplevel window
	top= tk.Toplevel(win)
	top.geometry("300x300")

	#Create a label to display warning
	label= tk.Label(top, text=warning_str)
	label.pack()

	#If there's an entry create an Entry Widget in the Toplevel window
	if with_entry:
		entry= tk.Entry(top, width= 25)
		entry.pack()
		return_val = entry.get()

		#Create a Button to print something in the Entry widget
		button= tk.Button(top, text="Ok", command=lambda:close_win(top))
		button.pack()
	else:
		return_val = None
	
	return return_val 

def decode_link_with_pop_up(link, win):
	"""
	Effectively decode_link function, but instead of printing the warning and inputting in the command line, 
	using this function will use tkinter to create a popup for entry
	:param: link str  - to be decoded
	:param: win tk.TK() - window to have pop up
	"""

	""" 
	Extract and parase meeting info from zoom url
	:param: 
		link str
	:return: 
		zoom_domain_name str
		password str
		conference_code str
	"""

	try:
		password = link.split('pwd=')[1]
	except: # error catching for not including password
		warning = "Password not found"
		pop_up_entry(win, warning)
		password = None

	try:
		conference_code = link.split('/j/')[1].split('?pwd=')[0]
	except: # error catching for not detecting conference code and allow for manual input
		warning = f"The conference code of {link} CAN NOT be detected. \nInput the conference code manually or click OK to continue anyway.\n"
		conference_code = pop_up_entry(win, warning, True)
		conference_code = "NOT FOUND" if conference_code == "" else conference_code.strip()
		if conference_code == "NOT FOUND":
			warning = f"The conference code of {link} CAN NOT be detected \nWill try joining this meeting with the original link. \nPlease ensure your browser will open the link with Zoom Client automatically."
			pop_up_entry(win, warning)
		else:
			warning = f"The conference code you entered is {conference_code}"
			pop_up_entry(win, warning)

	try:
		zoom_domain_name = link.split("//")[1].split("/j")[0]
	except:
		zoom_domain_name = ''
		warning = 'no domain name'
		pop_up_entry(win, warning)

	return zoom_domain_name, password, conference_code

class Meeting():
	"""
	A Meeting 
	Static:
	self.zoom_domain_name str
	self.password str
	self.conference_code str
	self.gui bool

	Methods:
	join(): detect operting system then join the meeting
	quit(): detect the operating system then kill the app
	"""
	def __init__(self, name, link, date, start_time, end_time, gui_window = None):
		self.name = name
		self.gui_window = gui_window
		try:
			self.start_time = convert_time(date, start_time)
			self.end_time = convert_time(date, end_time)
		except:
			warning = f'here is something wrong with your date or meeting time: \n name \n{date} \nmeeting time: \n {start_time} - {end_time}. \nIf you are expressing in day of week, it is case and typo sensitive. (e.g. Monday, Tuesday)'
			if gui_window is None:
				#print to command line
				print(bcolors.WARNING + warning +bcolors.ENDC)
			else:
				#pop up window for error
				pop_up_entry(gui_window, warning_str=warning, with_entry=False)
				
		self.zoom_domain_name, self.password, self.conference_code = decode_link(link) if gui_window is None else decode_link_with_pop_up(link, gui_window)
		self.link = link

	def join(self):
		"""
		detect operting system then join the meeting
		"""
		if platform.system() == 'Windows':
			if self.conference_code == "NOT FOUND":
				command = f'start {self.link}'  # using the original link to join
			else:
				command = f'start zoommtg://{self.zoom_domain_name}/join?confno={self.conference_code}?"&"pwd={self.password}'
		else:
			if self.conference_code == "NOT FOUND" :
				command = f'open {self.link}'  # using the original link to join
			elif self.password is None: # using the no passcode link to join
				command = f'open "zoommtg://{self.zoom_domain_name}/join?confno={self.conference_code}"'
			else: # joining normally
				command = f'open "zoommtg://{self.zoom_domain_name}/join?confno={self.conference_code}?&pwd={self.password}"'
		os.system(command)

	def quit(self):
		"""
		detect the operating system then kill the app #TODO end a specific meeting instead of killing the app and ending all meetings
		"""
		if platform.system() == 'Windows':
			os.system('taskkill /f /im Zoom.exe')
		else:
			os.system('killall zoom.us')