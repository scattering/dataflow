#import json
from django.utils import simplejson as json

a = open('../www/diagram/BT7example.json','r')

for line in a:
	json_obj = line

a.close()
print json.dumps(json_obj)
