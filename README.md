# Autozoom
--------
## What does it do and who is it for?

Autozoom is a super simple Python script to launch your Zoom meetings at the scheduled times, making sure you "showing up" on time, :wink:. 

There is no pip installation or dependency hell at all, so that it is easy to use for most of non-tech-savvy students/professionals. :man_student: :briefcase:

*"It is simplier than hosting a Minecraft server, kids"* :boy:

------
## Instructions
### Prerequisites
- Have [Python3](https://www.python.org/downloads/) installed. Make sure to pick the right version for you OS.
- Have [Zoom](https://zoom.us/download) client installed.
### How to start
1. `cd` into directory 
2. Edit the `schedule.csv` file formatted like the following:

| zoom-links |	date (blank for today) | meeting start time | meeting end time |
|--------------------------------------------------|--------|-----|-----|
|https://zoom.us/j/<conference_code>?pwd=<password>|		|09:45|10:30|
|https://zoom.us/j/<conference_code>?pwd=<password>|09/21/2020|12:45|13:30|
|https://zoom.us/j/<conference_code>?pwd=<password>|MM/DD/YYYY|HH:MM|HH:MM|
3. Be careful, the earliest meeting on top and in order. Make sure the formats are correct, and end time of each meeting is after the start time
4.  start the program `python auto-zoom.py` *(trick: if using non-Windows OS, do `screen python auto-zoom.py` instead and `CTR+A then D` to run in the background, or else you need to keep your terminal open)*

### Detailed instructions for first-timers
1. Have the prerequisites done
2. download the code from this page
3. find the folder where you downloaded to and unzip the file. Remenber the path (directory) where the file is located
4. then.....
#### If you are using a Mac :apple:
1. In Applications panel, find and open the **Terminal** app
2. In the **Terminal** type `cd your_path_to_the_folder` to cd into directory 
- ( if you don't know how to find the path, click the gear button :gear: on the top, and select *Copy "autozoom" as Pathname. )
- have something like`cd /Users/owl-dy/autozoom` in the **Terminal**, then hit *Enter*
3. Edit the `schedule.csv` file
4. In the **Terminal** start the program by typing `python auto-zoom.py`
#### If you are using a PC :computer:
1. In **Start** menu search of `cmd` and open it
2. In the **CMD** type `cd your_path_to_the_folder` to cd into directory 
- ( if you don't know how to find the path, in the folder, right-click > Properties > Locations is your path )
- have something like`cd /Users/owl-dy/autozoom` in the **CMD**, then hit *Enter*
3. Edit the `schedule.csv` file
4. In the **CMD** start the program by typing `python auto-zoom.py`

### autozoom-pro
check out `pro/` directory for more functionalities

## Other things about this project
### Inspiration & acknowledgement
- Inspired from this [CNET](https://www.youtube.com/watch?v=b-VCzLiyFxc) video
- I also saw a similar attempt on this [github repo](https://github.com/Kn0wn-Un/Auto-Zoom). However, his method uses image recognition, which requires some installations that are not so frindly to non-tech persons, and it only works on Windows. 
### Future stage (please join me!)
- Want to be able to have a trigger word for Zoom's audio output, so whenever you are called on, autozoom can play a pre-recorded audio file to fake your presence
- Want to redirect audio output to a NLP service, and play back pre-recorded audio based on the content of the input audio

