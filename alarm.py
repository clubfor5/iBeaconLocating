import _thread
import RPi.GPIO as GPIO
import time
def alarm(threadName, pin):
	GPIO.setwarnings(False)
	print("Alarm!")	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	for i in range(15):
		GPIO.output(pin, True)
		time.sleep(0.05)
		GPIO.output(pin, False)
		time.sleep(0.05)

def alarmShort(threadName, pin):
	GPIO.setwarnings(False)
	print("Alarm!")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)
	for i in range(5):
		GPIO.output(pin, True)
		time.sleep(0.05)
		GPIO.output(pin, False)
		time.sleep(0.05)

if __name__ == '__main__':
	alarm("ok",17)
