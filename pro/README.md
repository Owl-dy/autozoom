# Autozoom-pro
--------
## What does it do and who is it for? :cinema: :microphone:

Autozoom-pro is a slightly more advanced Python script to turn on your camera and audio and to play recorded script when joining the meetings. 
There are some Python packages and Zoom configurations required.

*"It is simplier than hosting a Minecraft server, kids"* :boy:

------
## Instructions
### Prerequisites
- Have [Python3](https://www.python.org/downloads/) installed. Make sure to pick the right version for you OS.
- Have [Zoom](https://zoom.us/download) client installed.
- Have your virtual background set to be a video of a fake you:
	- open an empty Zoom to record yourself
	- save the video
	- set the video as your vitual background
	- use a piece of tap to cover up your camera **VERY IMPORTANT FOR YOUR PRIVACY**
	- detailed steps about this hack, following this [link](https://lifehacker.com/how-to-create-a-looping-video-of-yourself-that-attends-1842843207) 
- [OPTIONAL] Record an audio which will be played on all Zoom meetings and save it as "audio_only.wav" (make sure is .wav format) in the same directory 
### Installation
Create a virtual environment and activate and pip install dependencies:

if Mac:apple:
```
cd autozoom/pro
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

if Windows:computer:
```
cd autozoom\pro
python -m virtualenv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```
### How to start
1. edit the `schedule.csv` file

|zoom-links|	date (in mm/dd/y format, leave it blank for today)|	meeting start time | meeting end time|	video?| audio?|
|------------------------------------|--|--------------------|-----------------|--------|-------|
|https://zoom.us/j/123456789?pwd=xxxx|  |14:03      |16:30                     |n       |   y   |
2. simply 
```
python auto-zoom-pro.py
```

## WARNINGS AND CAUTIONS :warning:
1. You will need to grant Terminal permission to use your mic and keyboard [link](https://pynput.readthedocs.io/en/latest/limitations.html#mac-osx)
	- System Preferences > Security&Privacy > Accessibility  > add Terminal (unlock with password to make changes)
2. You system will play the audio file that you requested to play, and the sound will be captured by your mic and send to Zoom. Make sure to put up a high volume so your mic can pick up the sound. 
	- soud redicting / looping app such as [Loopback](https://rogueamoeba.com/loopback/) for redirecting audio [TO BE TESTED]
3. **Very Important** to cover your camera with a tape. Virtual background can only be activated when camera is on.

## Future stage (please join me!)
- Want to be able to have a trigger word for Zoom's audio output, so whenever you are called on, autozoom can play a pre-recorded audio file to fake your presence
- Want to redirect audio output to a NLP service, and play back pre-recorded audio based on the content of the input audio

