import thread
import RPi.GPIO as GPIO
import time
def alarm(threadName, pin):
	GPIO.setwarnings(False)
	print("Alarm!")	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	for i in range(25):
		GPIO.output(pin, True)
		time.sleep(0.1)
		GPIO.output(pin, False)
		time.sleep(0.1)
	
if __name__ == '__main__':	
	alarm(17)
