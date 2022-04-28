
import RPi.GPIO as GPIO
import time
import os
from dotenv import load_dotenv

GPIO.setmode(GPIO.BOARD)
load_dotenv()
count = 0
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
    
    
def handle(pin):
    global count
    count = count + 1
    print ("interrupt fired" + str(count))
    

if (pinmode == "DOWN"):
    print("Listening to FALLING interrupt ON PIN")
    GPIO.add_event_detect(testpin, GPIO.FALLING, handle)
elif (pinmode == "UP"):
    print("Listening to RISING interrupt ON PIN")
    GPIO.add_event_detect(testpin, GPIO.FALLING, handle)
else:
    print("KINDLY SET TEST_PIN_MODE TO UP OR DOWN")
     


try:  
    while True : 
        # print (GPIO.input(testpin)) 
        time.sleep(0.5)
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