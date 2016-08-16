from omxplayer import OMXPlayer
import RPi.GPIO as GPIO
import time 

pulsePin = 26
hookPin = 19
resetPin = 17
debounceTime = 100

phoneNumLength = 4 
phoneNumber = []
number = 0
startTime = time.time()
player = OMXPlayer('./recordings/dialtone.wav')

GPIO.setmode(GPIO.BCM)
GPIO.setup(pulsePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(hookPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def count_pulse(channel):
	global startTime
	global number
	number = number + 1
	startTime = time.time()

def hook_event(channel):
	if GPIO.input(channel):
		GPIO.add_event_detect(pulsePin, GPIO.RISING, callback=count_pulse, bouncetime=debounceTime)
		print "RISING"
		global player
		player.play()

	else:
		global number 
		global phoneNumber
		number = 0
		phoneNumber = []
		GPIO.remove_event_detect(pulsePin)
		print "FALLING"
		player = OMXPlayer('./recordings/dialtone.wav')

GPIO.add_event_detect(hookPin, GPIO.BOTH, callback=hook_event, bouncetime=debounceTime)

while True:

	while (len(phoneNumber) != phoneNumLength):
		if ( (time.time() - startTime) > 0.5 and number != 0  ):
			print number
			phoneNumber.append(number)
			number = 0
		time.sleep(0.1) #Loop should not sample more than debounce time
	
	if ( len(phoneNumber) == phoneNumLength ):
		lastDigit = phoneNumber[-1]	
		if lastDigit == 1:
			print "Play Track 1"
			player.stop()
			time.sleep(0.1)
			player = OMXPlayer('./recordings/Aela.wav')
			player.play()
			player.action(16)
		elif lastDigit == 2:
			print "Play Track 2"
			player = OMXPlayer('./recordings/Rudy.wav')
			player.play()
		elif lastDigit == 3:
			print "Play Track 3"
			player = OMXPlayer('./recordings/imperial-march.mp3')
			player.play()
		elif lastDigit == 4:
			print "Play Track 4"
			player = OMXPlayer('./recordings/Maureen.wav')
			player.play()
		elif lastDigit == 5:
			print "Play Track 5"
			player = OMXPlayer('./recordings/Monty.wav')
			player.play()
		elif lastDigit == 6:
			print "Play Track 6"
			player = OMXPlayer('./recordings/Mariette.wav')
			player.play()
		else:
			print "No Track"
			player = OMXPlayer('./recordings/operator.wav')
			player.play()
		
		phoneNumber = []
