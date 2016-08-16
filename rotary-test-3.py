from omxplayer import OMXPlayer
import RPi.GPIO as GPIO
import time 

# Constants
pulsePin = 26
hookPin = 19
hookDebounce = 0.1
debounceTime = 100
pollInterval = 0.5
phoneNumLength = 4 
lastDigitPosition = -1

# Variables
state = 0
number = 0
phoneNumber = []
startTime = time.time()
lastPlay = 0
isInterrupt = False
player = OMXPlayer('./recordings/dialtone.wav')
player.set_volume(20000)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pulsePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(hookPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def countPulse(channel):
	global startTime
	global number
	number = number + 1
	startTime = time.time()

def selectRecording(number):
	if number == 1:
		print "Play Track 1"
		return './recordings/Aela.wav'
	elif number == 2:
		print "Play Track 2"
		return './recordings/Rudy.wav'
	elif number == 3:
		print "Play Track 3"
		return './recordings/imperial-march.mp3'
	elif number == 4:
		print "Play Track 4"
		return './recordings/Maureen.wav'
	elif number == 5:
		print "Play Track 5"
		return './recordings/Monty.wav'
	elif number == 6:
		print "Play Track 6"
		return './recordings/Mariette.wav'
	else:
		print "No Track"
		return './recordings/operator.wav'

# Continously run loop
while True:
	# Check for reset condition: receiver on hook
	if GPIO.input(hookPin) == False:
		time.sleep(hookDebounce)
		if GPIO.input(hookPin) == False:
			state = 0
	
	# init state: reset variables and remove interrupt if applicable
	if state == 0:
		number = 0
		phoneNumber = []
		if isInterrupt == True:
			GPIO.remove_event_detect(pulsePin)
			isInterrupt = False

		# check if the receiver is taken off the hook
		if GPIO.input(hookPin) == True:
			time.sleep(hookDebounce)
			state = 1
	
	# dial tone state: start interrupt, play dial tone
	elif state == 1:
		print "RESET"
		player.stop()
		player = OMXPlayer('./recordings/dialtone.wav')
		player.play()

		if isInterrupt == False:
			GPIO.add_event_detect(pulsePin, GPIO.RISING, callback=countPulse, bouncetime=debounceTime)
			isInterrupt = True

		state = 2
	
	# dial number state: fill phone number array with inputs from rotary dial
	elif state == 2:
		if len(phoneNumber) != phoneNumLength:
			if ( (time.time() - startTime) > pollInterval and number != 0 ):
				print number
				phoneNumber.append(number)
				number = 0
			time.sleep(hookDebounce)
		
		# when buffer is full, get the last digit
		elif len(phoneNumber) == phoneNumLength:
			lastDigit = phoneNumber[lastDigitPosition]
			phoneNumber = []
			state = 3
	
	# pick track state: based on the last digit, select a recording to play
	elif state == 3:
		recordingToPlay = selectRecording(lastDigit)
		player = OMXPlayer(recordingToPlay)
		player.play()
		state = 4
	
	# play state: recording plays until the reset condition is asserted
	elif state == 4:
		state = 4	

	else:
		state = 0

	# if there is motion detected, play video through HDMI in separate process
	# SUBPROCESS NOT WORKING
	#if GPIO.input(sensorPin) == False:
	#	if (time.time() - lastPlay) > clipDuration:
	#		print "motion detected"
	#		subprocess.call('omxplayer -o hdmi /home/pi/Desktop/recordings/imperial-march.mp3', shell=True)
	#		lastPlay = time.time()
					
