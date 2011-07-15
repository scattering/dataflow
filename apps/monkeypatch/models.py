from django.db import models
from django.db.models.signals import class_prepared

def longer_username(sender, *args, **kwargs):
	#print "NAME: ", sender.__name__, " MODULE: ", sender.__module__
	if sender.__name__ == "User" and sender.__module__ == "django.contrib.auth.models":
		sender.__meta.get_field("username").max_length = 254

# username.email is set as an EmailField

class_prepared.connect(longer_username)
