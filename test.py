
import RPi.GPIO as GPIO
import time
import os
from dotenv import load_dotenv

GPIO.setmode(GPIO.BOARD)
load_dotenv() 

testpin = int(os.getenv('TEST_PIN'))

pinmode = os.getenv('TEST_PIN_MODE') 

print(testpin)
if (pinmode == "UP"):
    print("setting testpin on pull-up mode")
    GPIO.setup(testpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
elif (pinmode == "DOWN"):
    print("setting testpin on pull-down mode")
    GPIO.setup(testpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
else:
    print("setting testpin on plain mode")
    GPIO.setup(testpin, GPIO.IN)
    
try:  
    while True : 
        print (GPIO.input(testpin)) 
        time.sleep(0.02)
except:
    GPIO.cleanup() 

# seamer 8
# testpin = 37
# GPIO.setup(testpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# counter2 = 33
# GPIO.setup(counter2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# seamer 7
# counter2 = 37
# GPIO.setup(testpin, GPIO.IN)