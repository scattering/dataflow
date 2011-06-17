import json
from django.utils import simplejson

a = open('../www/diagram/BT7example.json','r')

for line in a:
	json_obj = line

a.close()
print simplejson.dumps(json_obj)
