import time
import RPi.GPIO as GPIO          # Import GPIO library
GPIO.setmode(GPIO.BCM)           # Use GPIO pin/BCM numbering
for i in range(2,28):
    GPIO.setup(i, GPIO.OUT)      # Setup GPIO Pin 2 to 4 to OUT
while True:
    for i in range(2,28):
        GPIO.output(i,True)     # Turn on all the 3 LEDs
    time.sleep(1)               # Wait for one second
    for i in range(2,28):
        GPIO.output(i,False)    # Turn off all the 3 LEDs
    time.sleep(1)               # Wait for one second
