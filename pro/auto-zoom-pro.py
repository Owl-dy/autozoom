import csv, time, datetime, platform, os
from playsound import playsound
from utils import Meeting, Windows, Mac, bcolors

# consent to turn on camera and audio
consent = input(
    bcolors.WARNING + ' Would you like to turn on your camera or mic for the meetings? \n Please make sure virtual background is set up on Zoom \n Please make sure your audio file is named audio_only.wav in the same directory \n Do you consent? y/[N] \n' + bcolors.ENDC)
consent = True if consent.lower() == 'y' or consent.lower() == 'yes' else False

LATE_THRESHOLD = 0.5  # mins

if consent:
    VIDEO_TIME = int(input(bcolors.WARNING + ' How long would you loop your video for (mins)? \n' + bcolors.ENDC))  # mins --- to loop the virtual background
else:
    VIDEO_TIME = 0

##processing the csv and create a meeting list
meeting_list = []

my_path = os.path.abspath(os.path.dirname(__file__))
csv_path = os.path.join(my_path, "schedule.csv")
with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            line_count += 1
            meeting = Meeting(row[0], row[1], row[2], row[3], row[4], row[5])
            meeting_list.append(meeting)

    print(f'{bcolors.OKGREEN}Processed {line_count - 1} meetings. {bcolors.ENDC}')

# checking for the system
op = Windows() if platform.system() == 'Windows' else Mac()

# loop for checking meetings in the list
while len(meeting_list) > 0:
    # if the first meeting on the list (aka, the current meeting) is not yet started, wait
    if datetime.datetime.now() < meeting_list[0].start_time:
        while datetime.datetime.now() < meeting_list[0].start_time:
            # checking in interval until the meeting.start_time has past
            print(
                f'Currently is {datetime.datetime.now()}, and the next meeting is in {(meeting_list[0].start_time - datetime.datetime.now()).total_seconds() / 60} mins')
            time.sleep(LATE_THRESHOLD * 60)
        print(
            f'Currently is {datetime.datetime.now()}, {bcolors.OKGREEN}joining the meeting that starts at {meeting_list[0].start_time}......{bcolors.ENDC}')
        op.join(meeting_list[0])
        time.sleep(15)

        if consent:
            camera_open = False
            audio_open = False

            ## opening up camera
            if meeting_list[0].video:
                op.camera_action()  # open camera
                camera_open = True
                time.sleep(2)
            open_camera_time = time.time()  # timer for starting camera

            ## opening up audio
            if meeting_list[0].audio:
                op.audio_action()  # turn on audio
                audio_open = True

                try:
                    playsound('audio_only.wav')  # play the audio until finished
                except:
                    print(bcolors.WARNING +  'no audio to play' + bcolors.ENDC)

                if audio_open:
                    op.audio_action()  # mute
                    audio_open = False

            if camera_open:
                remaining_camera_time = VIDEO_TIME * 60 - (time.time() - open_camera_time)
                time.sleep(max(1, remaining_camera_time))  # keep camera open
                op.camera_action()  # turn off camera
                camera_open = False

    # if the current meeting is not yet over, sleep until the meeting ends
    meeting_remaining_time = (meeting_list[0].end_time - datetime.datetime.now()).total_seconds()
    if meeting_remaining_time > 0:
        print(f'Currently is {datetime.datetime.now()}, in session, and the meeting ends at {meeting_list[0].end_time}')
        time.sleep(meeting_remaining_time)

    # if the current time is after the ending time of the current meeting, exiting zoom and popping the meeting of the meeting list
    if datetime.datetime.now() > meeting_list[0].end_time:
        print(f'{bcolors.OKBLUE}Exiting meeting that ends at {meeting_list[0].end_time} {bcolors.ENDC}')
        op.quit()
        time.sleep(10)
        meeting_list.pop(0)
        print(f'{bcolors.OKGREEN}There are {len(meeting_list)} more meetings to be attended {bcolors.ENDC}')

    else:
        print(bcolors.FAIL + 'something wrong' + bcolors.ENDC)

print(bcolors.OKGREEN + 'Program finished... see you next time' + bcolors.ENDC)
