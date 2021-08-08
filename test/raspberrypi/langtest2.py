#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import lcddriver
import datetime
import Adafruit_BMP.BMP085 as BMP085

#display = lcddriver.lcd()
bmp085sensor = BMP085.BMP085()

from subprocess import call

def lcdPrint(text, linenum=1):
    global display
    display.lcd_display_string(text.ljust(16), linenum) 
def upload(key, value):
    print('/usr/bin/zabbix_sender','-c','/etc/zabbix/zabbix_agentd.conf', '-k',key, '-o', value)
    print call(['/usr/bin/zabbix_sender','-c','/etc/zabbix/zabbix_agentd.conf', '-k',key, '-o', str(value)])


def run_display():
    try:
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(11,4)
            #print 'Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature, humidity)
            lcdPrint("Temp   Humidity", 1) 
            lcdPrint('{0:0.1f} C {1:0.1f} %'.format(temperature, humidity), 2) 
            time.sleep(10)
            lcdPrint("Temp   Pressure", 1) 
            lcdPrint('{0:0.1f} C {1:0.1f} Pa'.format(bmp085sensor.read_temperature(), bmp085sensor.read_pressure()),2)
            time.sleep(10)
            lcdPrint("Alti   Sea Lev Alt", 1) 
            lcdPrint('{0:0.0f} m  {1:0.1f} Pa'.format(bmp085sensor.read_altitude(), bmp085sensor.read_sealevel_pressure()),2)
            time.sleep(10)

    finally:
        display.lcd_clear()


def run_zabbix():
    try:
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(11,4)
            pressure= bmp085sensor.read_sealevel_pressure()
            upload('sensor.humidity', humidity)
            upload('sensor.temperature', temperature)
            upload('sensor.pressure', pressure)
            time.sleep(60)

    finally:
        #display.lcd_clear()
        pass

if __name__ == '__main__':
    run_zabbix()
