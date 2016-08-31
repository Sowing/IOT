import mraa
import math
import time
import sys
import boto.dynamodb2
import thread
import threading
import pyupm_i2clcd as lcd
from boto import kinesis
from  threading import Timer
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER


def tempData():
    tempSensor = mraa.Aio(1)
    a = tempSensor.read()
    R = 1023.0/a-1.0
    R = 100000.0*R
    logd = math.log(R/100000.0)
    Celsius = 1.0/(logd/4275+1/298.15)-273.15
    tempInC = round(Celsius, 2)
    TempString = str(tempInC)
    print TempString
    #global t
    #t = RepeatableTimer(1, lambda:tempData())
    #t.start()
    #return TempString


def upload_db():
    tempData()
'''
    while(True):
        tempData()
        time.sleep(2)
'''

def upload_kinesis():
    while(True):
        tempData()
        time.sleep(2)


if __name__ == "__main__":
    switch_pin_number=8
    switch = mraa.Gpio(switch_pin_number)
    switch.dir(mraa.DIR_IN)
    myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
    myLcd.setColor(255, 255, 0)
    myLcd.setCursor(0, 0)
    myLcd.clear()
    print "ctrl+c to quit"
    i = 0
   # t1 = threading.Thread(target=upload_db())
   # t2 = threading.Thread(target=upload_kinesis())
    #global t
    timer = Timer(2, lambda: tempData())
    try:
        while(1):
            if (switch.read()):
                if (i == 1):
                    t1.suspend()
                    #timer.cancel()
                    #print timer.is_alive()
                    myLcd.clear()
                    myLcd.write("K")
                    i = 0
                    print "press2"
                    time.sleep(0.5)
                else:
                    print "press1"
                    myLcd.clear()
                    myLcd.write("D")
                    i = 1
                    t1 = threading.Thread(target=upload_db)
                    t1.daemon = True
                    t1.run()
                    #while(1):
                     #   timer.start()
                    #i = 1
                    #time.sleep(0.5)

    except KeyboardInterrupt:
        exit



