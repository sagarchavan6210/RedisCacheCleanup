#######################################################################
#Author: Sagar Chavan
#Azure Redis : Connect, Get, Set & Clean Cache Operation
#Usage: 
#	python RedisCleanup.py <Redis_Host> <RG_Name> <Subscription_ID>
#######################################################################

import pip
import redis
import sys
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from msrestazure.azure_active_directory import MSIAuthentication
from azure.mgmt.redis import RedisManagementClient

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
		
def connectRedis():
	creds = MSIAuthentication()
	resource_name = sys.argv[1]
	rg_name = sys.argv[2]
	subs_id = sys.argv[3]
	myHostname = resource_name+".redis.cache.windows.net"
	redis_client = RedisManagementClient(creds, subscription_id=subs_id)
	W_keys = redis_client.redis.list_keys(resource_group_name=rg_name, name=resource_name)
	#print(W_keys.primary_key)
	r = redis.StrictRedis(host=myHostname, port=6380,password=W_keys.primary_key,ssl=True)
	result = r.ping()
	print("Ping returned : " + str(result))
	
	if str(result) == "True":
		print ("connected to ",myHostname)
	
	result = r.set("Message", "The Redis cache is working with Python!")
	print("SET Message returned : " + str(result))

	result = r.get("Message")
	print("GET Message returned : " + result.decode("utf-8"))
	
	result = r.flushall()
	print ("Clean up status: " + str(result))
	
if __name__ == '__main__':
	#install('redis')
	connectRedis()	