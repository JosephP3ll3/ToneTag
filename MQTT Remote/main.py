# MIT License (MIT)
# Copyright (c) 2021 Mike Teachman
# https://opensource.org/licenses/MIT
from rotary_irq_rp2 import RotaryIRQ

from ePaper import EPD_2in9_Landscape

from machine import Pin

import time

# Wifi setup
import network
net = network.WLAN(network.STA_IF)
net.active(True)
net.connect("JP_Hotspot", "sdjc9588")
while net.isconnected() == False:
    print("Waiting for Connection")
    time.sleep(1)
print("Connected")

# MQTT
from umqtt.simple import MQTTClient
import binascii

mqtt_server = '72.208.203.48'
client_id = 'bigles'
topic_sub = b'Tone-Tag'


def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=0)
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


option = open('Options.txt','r')

entries = option.read().splitlines()

epd = EPD_2in9_Landscape()
epd.Clear(0xff)
epd.fill(0xff)
for i in range(0, len(entries)):
    epd.text(str(entries[i]),5, (10*i), 0x00)
epd.display(epd.buffer)
epd.delay_ms(2000)

r = RotaryIRQ(pin_num_clk=0,
              pin_num_dt=1,
              min_val=0,
              max_val=(len(entries)-1),
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP)

val_old = r.value()
    
# Pin Interupt
interrupt_flag=0
pin = Pin(2,Pin.IN,Pin.PULL_UP)
debounce_time=2
def pin_cb(pin):
    global interrupt_flag, debounce_time
    if (time.ticks_ms()-debounce_time) > 500:
        interrupt_flag= 1
        debounce_time=time.ticks_ms()
        
pin.irq(trigger=Pin.IRQ_FALLING, handler=pin_cb)   

while True:
    val_new = r.value()

    if val_old != val_new:
        epd.text('@' ,150, (10*val_old), 0xff)
        val_old = val_new
        epd.text('@' ,150, (10*val_new), 0x00)
        epd.display_Partial(epd.buffer)

    if interrupt_flag is 1:
        interrupt_flag = 0
        mes = entries[val_new]
        print(mes)
        client.publish(topic_sub, mes)
    
    time.sleep_ms(50)
