import mraa 
import math
import datetime 
import time 
import sys
import boto.dynamodb2 
import thread 
import threading 
import select
import json, base64
import pyupm_i2clcd as lcd 
from boto import kinesis 
from threading import Timer, Thread 
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex 
from boto.dynamodb2.table import Table 
from boto.dynamodb2.types import NUMBER 
from amazon_kclpy import kcl 
 
NEXT_STATE = 0
 
def tempData():
    try:
        tempSensor = mraa.Aio(1)
        a = tempSensor.read()
        R = 1023.0/a-1.0
        R = 100000.0*R
        logd = math.log(R/100000.0)
        Celsius = 1.0/(logd/4275+1/298.15)-273.15
        tempInC = round(Celsius, 2)
        TempString = str(tempInC)
        #print TempString
        return TempString
    except KeyboardInterrupt:
        sys.exit() 


def upload_db():
    try:
        data = tempData()
        t = datetime.datetime.now()
        tstr = str(t)
        table = Table('RoomTemp')
        table.put_item(data={'Time':tstr,'Temperature':data,
        })
	time.sleep(0.5)
        print "db"
    except KeyboardInterrupt:
        sys.exit()


def upload_kinesis():
    connection = kinesis.connect_to_region('us-east-1')
    tries = 0
    while tries < 10:
        tries += 1
        time.sleep(1)
        try:
            response = connection.describe_stream('Temperature')   
            if response['StreamDescription']['StreamStatus'] == 'ACTIVE':
                break 
        except KeyboardInterrupt:
            sys.exit()
            #logger.error('error while trying to describe kinesis stream : %s')
    else:
        raise TimeoutError('Stream is still not active, aborting...')
    
    data = tempData()
    print(data)
    try:
        connection.put_record("Temperature", json.dumps(data), "partitionkey")
    except IOError:
        print ErrorString
    except KeyboardInterrupt:
        sys.exit()
    #TO DO!!!!


def check_status():
    global NEXT_STATE, flag2
    try:
        while (flag2):
            if NEXT_STATE == 0:
                if switch.read():
                    NEXT_STATE = 1
                    #task_list.insert(0, 1) #test ues, ignore
                    time.sleep(0.6) # 0.5 sec to to allow main thread update the NEXT_STATE para
                else:
                    NEXT_STATE = 0
            elif NEXT_STATE == 1:
                if switch.read():
                    NEXT_STATE = 0
                    #task_list.insert(0, 0)
                    time.sleep(0.6)
                else:
                    NEXT_STATE = 1
        thread.exit() 
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    switch_pin_number=8
    switch = mraa.Gpio(switch_pin_number)
    switch.dir(mraa.DIR_IN)
    myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
    myLcd.setColor(255, 255, 0)
    myLcd.setCursor(0, 0)
    myLcd.clear()
    print "ctrl+c to quit"
    statusKey = 0
    previous_status = 0
    #task_list = [0]
    flag = True
    flag2 = True
    check_thread= Thread(target = check_status)
    check_thread.setDaemon = True
    check_thread.start()
    try:
        while (flag):
            if NEXT_STATE == 0:
                print "next state is ", NEXT_STATE
                myLcd.clear()
                myLcd.write("DynamoDB")
                upload_db()
                time.sleep(2) #same as time.sleep()
            elif NEXT_STATE == 1:
                print "next state is ", NEXT_STATE
                myLcd.clear()
                myLcd.write("Kinesis")
                upload_kinesis()
    except KeyboardInterrupt:
                print "exiting"
                flag2 = False
                sys.exit()
    sys.exit()
