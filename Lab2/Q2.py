from firebase import firebase
import json as simplejson
firebase = firebase.FirebaseApplication('https://fiery-inferno-4396.firebaseIO.com',None)
result  = firebase.get('',None)
print result
 
name = {'Pi':10, "edison90": 89}
#data = json.dumps(name)
 
post = firebase.post('',name)
 
print post

