import boto.sns
import logging
import sys

logging.basicConfig(filename = "sns-sqs-sub.log", level = logging.DEBUG)

c = boto.sns.connect_to_region("us-east-1")
topicarn = 'arn:aws:sns:us-east-1:850507712104:Demo_Topic'

def Switch_Stay():
    try:
        
    except IOError:
        print "Error measuring"
        return

if __name__ == "__main__":
    while (True):
        print 'Please select from the following options:'
        print '1.Plan trip (Will tell u if you should switch)'
        print '2.Subcribe to message feed:'
        print '3.Exit'
        command = raw_input('>>')
        try:
            if command == '1':
                Status = Switch_Stay()
                if Status:
                    print 'Switch'
                else:
                    print 'Stay'
            if command == '2':
                print 'Please enter your phone number'
                phone_number = raw_input('>>')
                subscription = c.subscribe(topicarn,"sms",phone_number)
                print subscription
            if command == '3':
                sys.exit()
        except KeyboardInterrupt:
            print "Error"
            sys.exit()
