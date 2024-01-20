import time
# Wifi Setup
import network
net = network.WLAN(network.STA_IF)
net.active(True)
net.connect("B77928", "E2T76B2B03343")
while net.isconnected() == False:
    print("Waiting for Connection")
    time.sleep(1)
print("Connected")


# MQTT Setup
from umqtt.simple import MQTTClient
import binascii

mqtt_server = '192.168.1.167'
client_id = 'smallles'
topic_sub = b'Tone-Tag'


def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()
    
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
#Pico Graphics Setup
import badger2040

badger = badger2040.Badger2040()
badger.clear()
badger.text("Testing",0,0,scale=2)
while True:
    client.subscribe(topic_sub)
    
    
