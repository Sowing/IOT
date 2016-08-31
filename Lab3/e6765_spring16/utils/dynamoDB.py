# 
#*********************************************************************************************
# Program to update dynamodb with latest data from mta feed. It also 
#cleans up stale entried from db
# Usage python dynamodata.py
# 
#*********************************************************************************************
import json,time,sys
from collections import OrderedDict
from threading import Thread

import boto3
from boto3.dynamodb.conditions import Key,Attr

sys.path.append('../utils')
import tripupdate,vehicle,alert,mtaUpdates,aws

### YOUR CODE HERE ####
from time import gmtime, strftime
import threading
import boto
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
from boto.dynamodb2.items import Item

def connection():
    ACCOUNT_ID = '850507712104'
    IDENTITY_POOL_ID = 'us-east-1:28a6696a-2293-4769-9e42-5accb12c2999'
    ROLE_ARN = 'arn:aws:cognito-identity:us-east-1:850507712104:identitypool/us-east-1:28a6696a-2293-4769-9e42-5accb12c2999'

    # Use cognito to get an identity.
    cognito = boto.connect_cognito_identity()
    cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
    oidc = cognito.get_open_id_token(cognito_id['IdentityId'])

    # Further setup your STS using the code below
    sts = boto.connect_sts()
    assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

    # Prepare DynamoDB client
    # Prepare DynamoDB client
    client_dynamo = boto.dynamodb2.connect_to_region(
        'us-east-1',
        aws_access_key_id=assumedRoleObject.credentials.access_key,
        aws_secret_access_key=assumedRoleObject.credentials.secret_key,
        security_token=assumedRoleObject.credentials.session_token)

    tables = client_dynamo.list_tables()
    dataTable = table_creation(tables, client_dynamo)
    return dataTable


def table_creation(tables, client_dynamo):
    if 'mtaIOT' not in tables['TableNames']:
        table = Table.create('mtaIOT', schema=[
            HashKey('tripId'),
        ], global_indexes=[
            GlobalAllIndex('EverythingIndex', parts=[
                HashKey('TimeStamp',data_type=NUMBER)]),
           GlobalAllIndex('EverythingIndex', parts=[
                HashKey('TimeStamp',data_type=NUMBER),
            ])
        ], connection=client_dynamo)
        
        time.sleep(5)

    else:
        table = Table('mtaIOT', connection=client_dynamo)
        time.sleep(0.1)

    return table


def formalize_data(mtaData, tripid, routeid, timestamp, startdate, direction, currentstopid, currentstopstatus, vehicletimestamp, futurestopdata, _TimeStamp):
    print mtaData, "hi"
    load = {
                        'tripId': tripid,
                        'routeId': routeid,
                        'dataTime':timestamp,
                        'startDate': startdate,
                        'direction': direction,
                        'currentStopId': currentstopid,
                        'currentStopStatus': currentstopstatus,
                        'vehicleTimeStamp': vehicletimestamp,
                        'futureStopData': futurestopdata,
                        'timeStamp': _TimeStamp
                }
    #data = json.dumps(load)
    item = Item(mtaData, load)
    return item
'''
    item = Item(mtaData, data={
                        'tripId': tripid,
                        'routeId': routeid,
                        'dataTime':timestamp,
                        'startDate': startdate,
                        'direction': direction,
                        'currentStopId': currentstopid,
                        'currentStopStatus': currentstopstatus,
                        'vehicleTimeStamp': vehicletimestamp,
                        'futureStopData': futurestopdata,
                        'timeStamp': _TimeStamp
                }
          )
'''
   # return item


def data_add(mtaData, mtaUpdateData):
    try:
        while(True):
            print "adding data"
            update_data = mtaUpdateData.getTripUpdates()
            _current_stop_id = None
            _current_stop_status = None
            _vehicle_time = None
            for update in update_data:
                _vehicle_time = None
            for update in update_data:
                if hasattr(update,'vehicleData'):
                    if hasattr(update.vehicleData,'currentStopId'):
                        _current_stop_id = update.vehicleData.currentStopId
                    if hasattr(update.vehicleData,'currentStopStatus'):
                        _current_stop_status = update.vehicleData.currentStopStatus
                    if hasattr(update.vehicleData,'timestamp'):
                        _vehicle_time = update.vehicleData.timestamp
                else:
                    _current_stop_id = None
                    _current_stop_status = None
                    _vehicle_time = None

            _trip_id = update.tripId
            _route_id = update.routeId
            _timestamp = time.time()
            _start_date = update.startDate
            _direction = update.direction
            _future_stops = update.futureStops
            _time_stamp = update.time
            print _time_stamp
            item_to_add = formalize_data(mtaData, _trip_id, _route_id, _timestamp, _start_date, _direction, _current_stop_id, _current_stop_status, _vehicle_time, _future_stops, _time_stamp)
            item_to_add.save(overwrite=True)
            time.sleep(30)
    except KeyboardInterrupt:
        print "user attemptted to exit"
        sys.exit()

def data_clean(mtaData):
    try:
        while(True):
            print 'cleaning data'
            response = mtaData.scan(dataTime__lte=(time.time()-120))
            for r in response:
                res = mtaData.delete_item(tripId=r['tripId'])
            time.sleep(60)
    except KeyboardInterrupt:
        print "user attemptted to exit"
        sys.exit()


if __name__ == "__main__":
    apikey = '78b884010b517f078fdaeb9345beac62'
    mtaUpdateData = mtaUpdates.mtaUpdates(apikey)
    mtaData = connection()
    print mtaData, "here"


    adding_thread = threading.Thread(target= data_add, args=(mtaData, mtaUpdateData, ))
    adding_thread.setDaemon(True)
    adding_thread.start()
    cleaning_thread = threading.Thread(target= data_clean, args=(mtaData,))
    cleaning_thread.setDaemon(True)
    cleaning_thread.start()
    try:
        while(1):
            pass
    except KeyboardInterrupt:
        sys.exit()
