import eel
import random
import time
from paho.mqtt import client as mqtt
import threading
import datetime
import RPi.GPIO as GPIO
import sys
import os
from dotenv import load_dotenv
from resetRpi import restart
from cleanchrome import cleanchrome
import json

cleanchrome()
eel.init('web')
load_dotenv()

canspercase = int(os.getenv('CANSPERCASE'))
team = 'group1'
target = int(os.getenv('TARGET_PER_MIN'))
shift = 'shift1'

broker = os.getenv('MQTT_SERVER')
port = os.getenv('MQTT_PORT')
dataTopic = os.getenv('DATA_TOPIC')
client_id = os.getenv('CLIENT_ID')
username = os.getenv('MQTT_USER')
password = os.getenv('MQTT_PASS')
resetTopic = os.getenv('RESET_TOPIC')
configTopic = os.getenv('CONFIG_TOPIC')
spaceTopic = os.getenv('SPACE_TOPIC')

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

counter1 = int(os.getenv('COUNTER1_PIN'))
previous1 = False
cnt1 = 0

counter2 = int(os.getenv('COUNTER2_PIN'))
previous2 = False
cnt2 = 0
cont2 = 0
downtime = 0
pr2 = 0
cspeed = 0
eque = []
eff = 0
avgLength = 0
delay = 0 
tstamp = 0
sleep_time = (100- int(os.getenv('CPU_USAGE', 95)))/100

now = datetime.datetime.now()

def setpinmode(PIN, pinmode):
    if (pinmode == "UP"):
        print("setting pin " + str(PIN) + " on pull-up mode")
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    elif (pinmode == "DOWN"):
        print("setting pin " + str(PIN) + " on pull-down mode")
        GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    else:
        print("setting PIN " + str(PIN) + " on plain mode")
        GPIO.setup(PIN, GPIO.IN)

setpinmode(counter1, os.getenv('COUNTER1_MODE') )
setpinmode(counter2, os.getenv('COUNTER2_MODE') )

@eel.expose
def set_pyconfigs(jclient_id, jteam, jcanspercase, jtarget):
    
    print("setting system defaults ...")
    eel.set_jsconfigs(jclient_id, jteam, jcanspercase, jtarget, getshift())
    print(getshift())
 
def countcans1():
    global cnt1, previous1, counter1, cnt2,avgLength
    threading.Timer(sleep_time, countcans1).start()
    if GPIO.input(counter1) == 1 and previous1 == False:
        cnt1 = cnt1 + 1
        # print("counter1 : " + str(cnt1))
        previous1 = True
    elif GPIO.input(counter1) == 0 and previous1 == True:
        previous1 = False
    avgLength = cnt1-cnt2  
       
def countcans2():
    global cnt1,cnt2, previous2, counter2, delay, downtime
    threading.Timer(sleep_time, countcans2).start()
    delay = delay + sleep_time
    if GPIO.input(counter2) == 1 and previous2 == False:
        cnt2 = cnt2 + 1
        # print("counter2 : " + str(cnt2))
        downtime = downtime + delay
        delay = 0
        previous2 = True
    elif GPIO.input(counter2) == 0 and previous2 == True:
        previous2 = False
        # set values to js  
    avgLength = cnt1-cnt2
    eel.set_metrics(cnt2, round(cnt2/canspercase,1), avgLength, round(downtime/60, 2), cnt1)
    
def getshift():
    if int(now.hour) in (6,7,8,9,10,11,12,13):
        return 'shift1'
    if  int(now.hour)  in (14,15,16,17,18,19,20,21):
        return 'shift2'
    if  int(now.hour)  in (22,23,0,1,2,3,4,5) :
        return 'shift3'
    


def on_connect(client, userdata, flags, rc):  
    global resetTopic,configTopic,spaceTopic
    client.subscribe(resetTopic)
    client.subscribe(configTopic)
    client.subscribe(spaceTopic)
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    global resetTopic,team,spaceTopic,eff,avgLength,downtime
    if msg.topic == resetTopic:
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        restart()
    if msg.topic == configTopic:
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        data = json.loads(msg.payload)
        team = data["team"]
    if msg.topic == spaceTopic:
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        data = json.loads(msg.payload)
        if data["clientID"] == client_id:
            fruitCount = int(data["fruitCount"])
            fruitLength = int(data["totalFruitLength"])
            eff = int(data["efficiency"])
            avgLength = int(data["averageFruitLength"])
            downtime = int(data["downtime"])
            eel.set_metrics(fruitLength, avgLength, downtime, fruitCount)
            eel.set_eff(eff)
            

client = mqtt.Client(os.getenv('CLIENT_ID'))  # 
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
username = os.getenv('MQTT_USER')
password = os.getenv('MQTT_PASS')
client.username_pw_set(username, password)
client.connect(os.getenv('MQTT_SERVER'))
client.loop_start()  #Start loop


def publish():
    global client, cnt1, cnt2, cont2, downtime, avgLength
    msg = '{"clientID":"'+ str(client_id) +'","target":"'+ str(target) +'","cans":" ' + str(cnt2) + '","canspercase":"' + str(canspercase) + '","cases":"' + str(round(cnt2/canspercase,1)) + '","cspeed":"'+ str(cspeed * 60) +'","tstamp":"'+str(tstamp) +'","avgLength":"'+str(avgLength)+'","downtime":"'+str(downtime)+'"}'
    topic = dataTopic
    result = client.publish(topic, msg)
    status = result[0] 
    # if status != 0:
        # print("publish() returned error code:" + str(result))
        
    
def sendcans():
    global cnt2, downtime, pr2, cspeed, canspercase, tstamp
    threading.Timer(1.0, sendcans).start()
    cspeed = cnt2 - pr2
    pr2 = cnt2
    eque.append(cspeed)
    if len(eque) < 5 :
        eque.append(cspeed)
    else :
        eque.pop(0)
    eff = round((sum(eque)*12 / target)*100, 1)
    eel.set_eff(eff)
    publish()
    tstamp = tstamp + 1


set_pyconfigs(client_id, team, canspercase, target)


print("counter1 : " + os.getenv('COUNTER1_STATUS') + " counter2 : " + os.getenv('COUNTER2_STATUS'))
print(spaceTopic)

if os.getenv('COUNTER1_STATUS') == "ENABLED":
    countcans1()
if os.getenv('COUNTER2_STATUS') == "ENABLED":
    countcans2()
    
if os.getenv('COUNTER2_STATUS') == "ENABLED" or os.getenv('COUNTER1_STATUS') == "ENABLED":
    sendcans()  

eel.start('index.html', host='localhost', port=27011, size=(1280,960), position=(0,0), cmdline_args=['--disable-infobars','--start-fullscreen'] )
