"""
This code was typed up and ran using nano on the raspberry pi
Instead of pushing it to github this file was copy and pasted on to github.
Because of this, the spacing/indentation can be a little wonky if you modify it
"""

import time
import grovepi
import RPi.GPIO as GPIO
from grove_rgb_lcd import *
from time import sleep

import paho.mqtt.client as mqtt
#import time
from datetime import datetime
import socket



#connect to any i2c
lcd = 3

#grovepi.pinMode(potentiometer, "INPUT")
grovepi.pinMode(lcd, "OUTPUT")
time.sleep(1)


#set the bus and connect the ultrasound sensor to D4
grovepi.set_bus("RPI_1")
ultrasound_sensor = 4

# Setting up the LCD
lcd = 0x3f
setRGB(0, 255, 0)

# Setting up LEDs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(10, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(12, GPIO.OUT, initial = GPIO.HIGH)


#Setting up MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect("172.20.10.4",1883,60)


mqtt_client.loop_start()
time.sleep(1)


while True:
   try:
   
      # Read sensor value from potentiometer
      ultrasound_range = grovepi.ultrasonicRead(ultrasound_sensor)
      #mqtt_client.publish("parking/sensor", ultrasound_range)

      #Check if object is within threshold distance
      if (ultrasound_range >= 25):
         mqtt_client.publish("parking/sensor","In the clear: "+f"{ultrasound_range}")
         setRGB(0, 255,0)
         GPIO.output(12, GPIO.LOW)
         GPIO.output(8, GPIO.HIGH)
         GPIO.output(10, GPIO.HIGH)
         setText_norefresh(str("You have space! space left: " + str(ultrasound_range)+ "cm"))
      elif (ultrasound_range >= 10 and ultrasound_range < 25):
        #yellow
         mqtt_client.publish("parking/sensor","Getting close: "+ f"{ultrasound_range}")
         setRGB(252, 213, 0)
         GPIO.output(12, GPIO.HIGH)
         GPIO.output(8, GPIO.HIGH)
         GPIO.output(10, GPIO.LOW)
         setText_norefresh(str("Slow down! space left: " + str(ultrasound_range)+ "cm"))
      else:
         mqtt_client.publish("parking/sensor","Almost hitting curb: "+f"{ultrasound_range}")
         setRGB(255, 0, 0)
         GPIO.output(12, GPIO.HIGH)
         GPIO.output(8, GPIO.LOW)
         GPIO.output(10, GPIO.HIGH)
         setText_norefresh(str("STOP! space left: " + str(ultrasound_range)+"cm"))

   except KeyboardInterrupt:
       break
   time.sleep(0.2)

mqtt_client.loop_stop()
mqtt_client.disconnect()

