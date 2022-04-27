import eel
from paho.mqtt import client as mqtt
import threading
import time
from getshift import getshift
from gethourly import hcases
import os
from dotenv import load_dotenv
from resetRpi import restart
from cleanchrome import cleanchrome

cleanchrome()

eel.init('web')
load_dotenv()
def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    # print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe(os.getenv('DATA_TOPIC'))  # Subscribe to the topic “digitest/test1”, receive any messages published on it
    client.subscribe(os.getenv('RESET_TOPIC'))

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    # print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    if msg.topic == os.getenv('RESET_TOPIC'):
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        restart()
            
            
    if msg.topic == os.getenv('DATA_TOPIC'): 
        eel.set_metrics(str(msg.payload))
    

client = mqtt.Client(os.getenv('CLIENT_ID'))  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
username = os.getenv('MQTT_USER')
password = os.getenv('MQTT_PASS')
client.username_pw_set(username, password)
print(os.getenv('MQTT_PORT'))
client.connect(os.getenv('MQTT_SERVER'))
client.loop_start()  #Start loop

def messageSender(msg):
    topic = os.getenv('DATA_TOPIC')
    result = client.publish(topic, msg)
    status = result[0]
    if status != 0:
        print(str(status) + "Failed to send message to topic")
    


# {"clientID":"L1","cans":"0","packs":"0","lcases":"0","cases":"0","lspeed":"0","tstamp":"13917942","targetcases":"240","canspercase":"24","unitspercase":"1","hr_output":"0,0,0,0,0,0,0,0,0"}

@eel.expose
def set_pyconfigs():
    client_id = os.getenv('CLIENT_ID')
    left = os.getenv('LEFT')
    right = os.getenv('RIGHT')
    target_l = os.getenv('TARGET_L')
    target_r = os.getenv('TARGET_R')
    print("setting pyconfigs")
    eel.set_jsconfigs(client_id, left, right, target_l, target_r)



@eel.expose
def get_hcases():
    lcase = hcases(os.getenv('LEFT'))
    rcase = hcases(os.getenv('RIGHT'))
    try:
        eel.hcases_left(lcase)
    except:
        print(str(os.getenv('LEFT')) + ": Could not render hourly cases: " + str(lcase))
    time.sleep(5)
    
    try: 
        eel.hcases_right(rcase)
    except:
        print(str(os.getenv('LEFT')) + ": Could not render hourly cases: " + str(rcase))
    
    
   

eel.start('index.html', host='localhost', port=27011, size=(1280,960), position=(0,0), cmdline_args=['--disable-infobars','--Kiosk'] )
