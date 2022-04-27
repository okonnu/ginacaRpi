
from paho.mqtt import client as mqtt
from app import messageAction
import os
from dotenv import load_dotenv
from resetRpi import restart



def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    # print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe(os.getenv('DATA_TOPIC'))  # Subscribe to the topic “digitest/test1”, receive any messages published on it
    client.subscribe(os.getenv('DATA_TOPIC'))

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    # print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    messageAction(str(msg.payload))
    

client = mqtt.Client(os.getenv('CLIENT_ID'))  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
username = os.getenv('MQTT_USER')
password = os.getenv('MQTT_PASS')
client.username_pw_set(username, password)
client.connect(os.getenv('MQTT_SERVER'), os.getenv('MQTT_PORT'), os.getenv('MQTT_KEEP_ALIVE'))
client.loop_start()  #Start loop

def messageSender(msg):
    topic = os.getenv('DATA_TOPIC')
    result = client.publish(topic, msg)
    status = result[0]
    if status != 0:
        print(str(status) + "Failed to send message to topic")
    
