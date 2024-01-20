import time
# Wifi Setup
import network
import gc
gc.collect()
net = network.WLAN(network.STA_IF)
net.active(True)
net.connect("JP_Hotspot", "sdjc9588")
while net.isconnected() == False:
    print("Waiting for Connection")
    time.sleep(1)
print("Connected")

#Pico Graphics Setup
import badger2040
badge = badger2040.Badger2040()


# MQTT Setup
from umqtt.simple import MQTTClient
import binascii

mqtt_server = '72.208.203.48'
client_id = 'smallles'
topic_sub = b'Tone-Tag'


def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    parts = msg.split()
    badge.set_pen(15)
    badge.clear()
    badge.set_pen(0)
    badge.text(parts[0],0,0,scale=5)
    badge.text(parts[1],0,40,scale=5)
    badge.update()
    

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
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


while True:
    client.subscribe(topic_sub)
    gc.collect()
#     client.ping()
#     client.check_msg() 
    pass
    
    
 