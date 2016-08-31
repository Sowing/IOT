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
assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

client_dynamo = boto.dynamodb2.connect_to_region(
    'us-east-1',
    aws_access_key_id=assumedRoleObject.credentials.access_key,
    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
    security_token=assumedRoleObject.credentials.session_token)


CUTable = Table.create("CUTable", schema =[
		HashKey('Sex'),
		RangeKey('CUID'),
	], throughput = {
		'read':10,
		'write':10,
	}, indexes=[
	    KeysOnlyIndex('NameRelateToSex', parts=[
		HashKey('Sex'),
		RangeKey('First_Name'),
		]),
	], global_indexes=[
	GlobalAllIndex('First_NameAndCUID', parts=[
		HashKey('First_Name'),
		RangeKey('CUID'),
	],
	throughput={
		'read':5,
		'write':5,
	})
	],	
	connection = client_dynamo
	) 
