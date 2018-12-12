import time
import RPi.GPIO as GPIO      # Import GPIO library
GPIO.setmode(GPIO.BCM)       # Use GPIO pin/BCM numbering
GPIO.setup(2, GPIO.OUT)      # Setup GPIO Pin 2 to OUT
while True:
	GPIO.output(2,True)   # Turn on LED
	time.sleep(1)         # Wait for one second
	GPIO.output(2,False)  # Turn off LED
	time.sleep(1)         # Wait for one second
