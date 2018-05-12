#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import lcddriver
import datetime

display = lcddriver.lcd()

try:
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(11,4)
		#print 'Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature, humidity)
		display.lcd_display_string("Temp   Humidity", 1) 
		display.lcd_display_string('{0:0.1f} C {1:0.1f} %'.format(temperature, humidity), 2) 
		time.sleep(2)

finally:
	display.lcd_clear()
