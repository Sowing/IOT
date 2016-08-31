import sys
import time
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER


def add_item(new_item, target_table):
    try:
        table = Table(target_table)
        table.put_item(data=new_item)
        time.sleep(0.5)
        return
    except IOError:
        print "Error adding item"
        return

#def delete_tem(item_to_delete, target_table):
#	try:
   #     table = Table(target_table)
    #    table.delete_item(item_to_delete)
        #TODO!!!
     #   time.sleep(0.5)
     #   return
   # except IOError:
    #	print "Error deleting item"
    #	return


#def view_table(target_table):
#	try:
		#CHANGE HERE!!!!
#        table = Table(target_table)
#        result_set = table.scan()
 #       for user in result_set:
  #          print user['first_name']
  #  except IOError:
   # 	print "Error viewing items"
    #	return


#def func_search(target_table, target_index):
#	try:
#        table = Table(target_table)
#        _index = target_index
#        #TODO

#        print "result is: "
#    except IOError:
#    	print "Error searching item!"



if __name__ == "__main__":
        flag = True
        print "please enter commands 'add<>to<>' or 'delete<>from<>' or 'view<>' or 'search<>by<>'"
        while (flag):
                print "Commands:"
                raw = raw_input('>>')
                command = raw.split()
                try:
                    	if command[0] == "add" and len(command) == 4:
                                print "Sex:"
                                input_0 = raw_input('>>')
                                print "CUID:"
                                input_1 = raw_input('>>')
                                print "First_Name:"
                                input_2 = raw_input('>>')
                                print "Last_Name:"
                                input_3 = raw_input('>>')
                                new_item = {'Sex':input_0,'CUID':input_1,'First_Name':input_2,'Last_Name':input_3,}
                                target_table = command[3]
                                print "adding item"
                                add_item(new_item, target_table)
                        elif command[0] == "delete" and len(command) == 4:
# 				command[1].delete()                       
                                table = Table(command[3])
				print "Sex:"
				input_0 = raw_input('>>')
				print "CUID:"
				input_1 = raw_input('>>')
				print "First_Name:"
				input_2 = raw_input('>>')
				print "Last_Name:"
				input_3 = raw_input('>>')
 
table.delete_item(Sex=input_0,CUID=input_1,First_Name=input_2,Last_Nameinput_3)

                                print "run deleting function"
                        elif command[0] == "view" and len(command) == 2:
                                target_table = command[1]
                                view_table(target_table)
                                print "view data"
                        elif command[0] == 'exit':
                                print "exiting"
                                time.sleep(1)
                                sys.exit()
                        elif command[0] == 'search':
                                target_table = command[1]
                                target_index = command[3]
                                print "searching...."
                        else:
                             	print "invalid command!"

                except KeyboardInterrupt:
                        print "exiting"
                        sys.exit()
