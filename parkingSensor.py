"""
This code was typed up and ran using nano on the raspberry pi 
Instead of pushing it to github this file was copy and pasted on to github.
Because of this, the spacing/indentation can be a little wonky if you modify it and don't use the correct # of spaces
"""

import time
import grovepi
import RPi.GPIO as GPIO
from grove_rgb_lcd import *
from time import sleep

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

while True:
   try:

      # Read sensor value from potentiometer
      ultrasound_range = grovepi.ultrasonicRead(ultrasound_sensor)

      #Check if object is within threshold distance
      if (ultrasound_range >= 25):
         setRGB(0, 255,0)
         GPIO.output(12, GPIO.LOW)
         GPIO.output(8, GPIO.HIGH)
         GPIO.output(10, GPIO.HIGH)
         setText_norefresh(str("You have space! space left: " + str(ultrasound_range)+ "cm"))
      elif (ultrasound_range >= 10 and ultrasound_range < 25):
        #yellow
         setRGB(252, 213, 0)
         GPIO.output(12, GPIO.HIGH)
         GPIO.output(8, GPIO.HIGH)
         GPIO.output(10, GPIO.LOW)
         setText_norefresh(str("Slow down! space left: " + str(ultrasound_range)+ "cm"))
      else:
         setRGB(255, 0, 0)
         GPIO.output(12, GPIO.HIGH)
         GPIO.output(8, GPIO.LOW)
         GPIO.output(10, GPIO.HIGH)
         setText_norefresh(str("STOP! space left: " + str(ultrasound_range)+"cm"))

   except KeyboardInterrupt:
       break
   time.sleep(0.2)
