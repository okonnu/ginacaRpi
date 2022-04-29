
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(13,GPIO.OUT)


def probeLight(eff):
    if eff < 60:
        GPIO.output(13,True)
    else:
        GPIO.output(13,False)