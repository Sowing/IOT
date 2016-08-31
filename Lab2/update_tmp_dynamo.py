import boto
import boto.dynamodb2
import time
import datetime
import mraa
import math
import sys
import boto.dynamodb2
import thread
import threading
import json
import base64
import pyupm_i2clcd as lcd
from boto import kinesis
from  threading import Timer, Thread
from amazon_kclpy import kcl
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
#users = Table.create('users', schema=[HashKey('username')]);

ACCOUNT_ID = '850507712104'
IDENTITY_POOL_ID = 'us-east-1:28a6696a-2293-4769-9e42-5accb12c2999'
ROLE_ARN = 'arn:aws:iam::850507712104:role/Cognito_edisonDemoKinesisUnauth_Role'
DYNAMODB_TABLE_NAME = 'edisonDemoDynamo'

# Use cognito to get an identity.
cognito = boto.connect_cognito_identity()
cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
oidc = cognito.get_open_id_token(cognito_id['IdentityId'])
 
# Further setup your STS using the code below
sts = boto.connect_sts()
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", 
oidc['Token'])

client_dynamo = boto.dynamodb2.connect_to_region(
    'us-east-1',
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)

def tempData():
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
    except IOError:
        print "Error adding item"
        return
    #TO DO!!!!

if __name__ == "__main__":
        flag = True
        print "Start adding temperature to table"
        while(flag):
            try:
                tempData()
                upload_db()
            except KeyboardInterrupt:
                print "exiting"
                sys.exot()

