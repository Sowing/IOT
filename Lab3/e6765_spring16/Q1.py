import google.protobuf
import vehicle, alert, tripupdate
import gtfs_realtime_pb2
import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict
from pytz import timezone

class mtaUpdates(object):

    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')

    # feed url depends on the routes to which you want updates
    # here we are using feed 1 , which has lines 1,2,3,4,5,6,S
    # While initializing we can read the API Key and add it to the url
    feedurl = 'http://datamine.mta.info/mta_esi.php?feed_id=1&key='

    VCS = {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"}
    tripUpdates = []
    alerts = []

    def __init__(self,apikey):
        self.feedurl = self.feedurl + apikey

    # Method to get trip updates from mta real time feed
    def getTripUpdates(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            with contextlib.closing(urllib2.urlopen(self.feedurl)) as response:
                d = feed.ParseFromString(response.read())
        except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
            print "Error while connecting to mta server " +str(e)

        timestamp = feed.header.timestamp
        nytime = datetime.fromtimestamp(timestamp,self.TIMEZONE)

        for entity in feed.entity:
            # Trip update represents a change in timetable
            if entity.trip_update and entity.trip_update.trip.trip_id:
                update = tripupdate.tripupdate()
                ##### INSERT TRIPUPDATE CODE HERE ####
                header_time = feed.header.timestamp
                update.tripId = entity.trip_update.trip.trip_id
                update.routeId = entity.trip_update.trip.route_id
                update.startDate = entity.trip_update.trip.start_date
                directionId = update.tripId.rfind('.')
                directionInt = int(directionId)

                update.direction = update.tripId[int(directionInt+1):int(directionInt+2)]
                update.time = header_time
                update.futureStops = OrderedDict()

                for stop in entity.trip_update.stop_time_update:
                    stopId = stop.stop_id
                    stopInfo = OrderedDict()
                    stopInfo['arrivalTime'] = stop.arrival.time
                    stopInfo['departureTime'] = stop.departure.time
                    stopInfo['arrivalTime'] = stop.arrival.time
                    stopInfo['departureTime'] = stop.departure.time
                    update.futureStops[stopId] = stopInfo
                    #print "check1"
                self.tripUpdates.append(update)
                    #print self.tripUpdates

            if entity.vehicle and entity.vehicle.trip.trip_id:
                v = vehicle.vehicle()
                ##### INSERT VEHICLE CODE HERE #####
                header_time_v = entity.vehicle.timestamp
                v.currentStopNumber = entity.vehicle.current_stop_sequence
                v.currentStopId = entity.vehicle.stop_id
                v.timestamp = header_time_v
                v.currentStopStatus = entity.vehicle.current_status

                for trip in self.tripUpdates:
                    if trip.tripId == entity.vehicle.trip.trip_id:
                        trip.vehicleData = v
                        #print "check2"

            if entity.alert:
                a = alert.alert()
                #### INSERT ALERT CODE HERE #####
                if entity.alert and entity.alert.header_text and entity.alert.header_text.translation and hasattr(entity.alert.header_text.translation,'text'):
                    a.alertMessage = entity.alert.header_text.translation.text
                if entity.alert and entity.alert.informed_entity and hasattr(entity.alert.informed_entity,'trip'):
                    if hasattr(entity.alert.informed_entity.trip,'trip_id'):
                        a.tripId = entity.alert.informed_entity.trip.trip_id
                        for tripUpdate in self.tripUpdates:
                            if tripUpdate.tripId == entity.alert.informed_entity.trip.trip_id:
                                a.startDate = tripUpdate.startDate
                    if entity.alert.informed_entity.trip.route_id:
                        a.routeId = entity.alert.informed_entity.trip.route_id
                        #print "check3"

                self.alerts.append(a)

        return self.tripUpdates
        # END OF getTripUpdates method

'''
if __name__ == "__main__":
    apikey = '20778f9857669c6fdf7fbd4e4f07fd30'
    update_data = mtaUpdates(apikey)
    update_data.getTripUpdates()
'''
