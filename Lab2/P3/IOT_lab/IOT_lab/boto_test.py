import sys
import time
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

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

def add_item(new_item, target_table):
    try:
        table = Table(target_table)
        table.put_item(data=new_item)
        time.sleep(0.5)
        return
    except IOError:
        print "Error adding item"
        return

def delete_item(target_table, target_item):
        try:
            table = Table(target_table)
            to_del = table.get_item(CUID = target_item)
            to_del.delete()
            time.sleep(0.5)
            return
        except IOError:
            print "Error deleting item"
            return


def view_table(target_table):
	try:
		#CHANGE HERE!!!!
            table = Table(target_table)
            result_set = table.scan()
            for user in result_set:
                print user['CUID'], ":", user["First_Name"], " ", user["Last_Name"]
        except IOError:
            print "Error viewing items"
            return


def func_search(target_table, target_index_1, target_index_2):
	try:
            table = Table(target_table)
            _index = target_index_1
            if target_index_1 == 'CUID':
                result_list = table.query_2(
                    CUID__eq=target_index_2,
                 )
#                print dict(result_list)
            elif target_index_1 == 'First_Name':
                result_list = table.scan(
                    First_Name__eq=target_index_2,
                    )
            for user in result_list:
                print user['CUID'], ":", user['First_Name'], " ", user['Last_Name']
                    

          #  print "result is: "
        except IOError:
            print "Error searching item!"



if __name__ == "__main__":
        flag = True
        print "please enter commands 'add<>to<>' or 'delete<>from<>' or 'view' or 'search<>by<><>'"
        while (flag):
                print "Commands:"
                raw = raw_input('>>')
                command = raw.split()
                try:
                    	if command[0] == "add" and len(command) == 4:
                                print "CUID:"
                                input_1 = raw_input('>>')
                                print "First_Name:"
                                input_2 = raw_input('>>')
                                print "Last_Name:"
                                input_3 = raw_input('>>')
                                new_item = {'CUID':input_1,'First_Name':input_2,'Last_Name':input_3,}
                                target_table = command[3]
                                print "adding item"
                                add_item(new_item, target_table)
                        elif command[0] == "delete" and len(command) == 4: 
                                target_item = command[1]
                                target_table = command[3]
                                print "run deleting function"
                                delete_item(target_table, target_item)
                        elif command[0] == "view" and len(command) == 2:
                                target_table = command[1]
                                #key = command[3]
                                view_table(target_table)
                        elif command[0] == 'exit':
                                print "exiting"
                                time.sleep(1)
                                sys.exit()
                        elif command[0] == 'search':
                                target_table = command[1]
                                target_index_1 = command[3]
                                target_index_2 = command[4]
                                print "searching...."
                                func_search(command[1],command[3],command[4])
                        else:
                             	print "invalid command!"

                except KeyboardInterrupt:
                        print "exiting"
                        sys.exit()
