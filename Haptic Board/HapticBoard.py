from omxplayer.player import OMXPlayer
import sys
from time import sleep
from threading import Lock, Thread
import RPi.GPIO as GPIO

def on_press(channel):
	global lastchannelpressed
	lastchannelpressed = channel
	global currentIndex
	global lock
	if(not lock.locked()):
		lock.acquire()
		global player
		global killed
		global videotochannelmap
		if(channel is 4):
			killed = True
			for videoplayer in player.values():
				videoplayer.exitEvent = lambda arg1, arg2: blank()
				videoplayer.quit()
			GPIO.cleanup()
			sys.exit(0)
		else:
			changeTo(videotochannelmap[channel])
		lock.release()
		if(currentIndex != videotochannelmap[lastchannelpressed]):
			on_press(lastchannelpressed)

def set_layer_video(vidindex, layer):
	global player
	if(vidindex is not 0):
		player[vidindex].set_layer(layer)

def changeTo(videoIndex):
	global currentIndex
	if(videoIndex == currentIndex):
		player[currentIndex].set_position(0)
	else:
		player[videoIndex].play()
		set_layer_video(videoIndex, 3)
		set_layer_video(currentIndex, 1)
		set_layer_video(videoIndex, 4)
		player[currentIndex].exitEvent = lambda arg1, arg2: blank()
		player[currentIndex].quit()
		player[currentIndex]= newVideoInit(currentIndex)
		currentIndex = videoIndex

def initNew(videoIndex):
	player[videoIndex] = newVideoInit(videoIndex)

def blank():
	pass

def playBackground():
	global player
	global currentIndex
	player[0].play()
	player[currentIndex] = newVideoInit(currentIndex)
	currentIndex = 0

def newVideoInit(videoIndex):
	if(videoIndex is not 0):
		#--live(did not work) --threshold (s) --video_queue (mb)
		y= OMXPlayer(files[videoIndex], args=['--no-keys','--no-osd', '-b', '--layer', '1', '--video_queue', '1', '-n', '-1'], dbus_name='omxplayer.player'+str(videoIndex), pause=True)
		y.exitEvent = lambda arg1, arg2: playBackground()
		return y
	else:
		#as hack to keep aspect ratio --win and then calculate --aspect-mode letterbox does not work
		return OMXPlayer(files[videoIndex], args=['--no-keys','--no-osd', '-b','--layer', '2', '--video_queue', '1', '-n', '-1', '--loop'], dbus_name='omxplayer.player'+str(videoIndex),pause=True)

#omxplayer only allows 8 processes
files = {
0: '/home/pi/Videos/vid0.mp4',
1: '/home/pi/Videos/vid1.mp4',
2: '/home/pi/Videos/vid2.mp4',
3: '/home/pi/Videos/vid3.mp4',
4: '/home/pi/Videos/vid4.mp4',
5: '/home/pi/Videos/vid5.mp4',
6: '/home/pi/Videos/vid6.mp4',
7: '/home/pi/Videos/vid7.mp4',
}

videotochannelmap = {
2: 1,
3: 2,
4: 'used to exit out',
17: 3,
27: 4,
22: 5,
26: 7,
19: 6,
}

lock = Lock()

global player

player = {
0: newVideoInit(0),
1: newVideoInit(1),
2: newVideoInit(2),
3: newVideoInit(3),
4: newVideoInit(4),
5: newVideoInit(5),
6: newVideoInit(6),
7: newVideoInit(7),
}


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def on_press_parallel(channel):
	p=Thread(target=on_press, args=(channel,))
	p.start()

for gpiopin in videotochannelmap.keys():
	GPIO.setup(gpiopin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(gpiopin, GPIO.FALLING, callback=on_press_parallel, bouncetime=300)

global currentIndex
global killed
killed = False
lastchannelpressed=0

player[0].play()
currentIndex = 0

#Keep Thread alive
while not killed:
	try:
		sleep(1000)
	except KeyboardInterrupt:
		on_press(4)


