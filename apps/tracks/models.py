from django.db import models
from django.contrib.auth.models import User, Permission

# Create your models here.

class Test(models.Model):
	field1 = models.CharField(max_length=200)
	field2 = models.IntegerField()
	def __unicode__(self):
		return self.field1

# class User     is provided by contrib.auth

class Userprofile(models.Model):
	userdisplay = models.CharField(max_length=300)

# class Permission     is provided by contrib.auth

class File(models.Model):
	permissions = models.ForeignKey(Permission) #or should this be a string of permission names
	name = models.CharField(max_length=160, primary_key=True) # what format are we storing the contents in?
	location = models.CharField(max_length=300) #location of file on disc
	metadata = models.ManyToManyField('Metadata')
	
class Metadata(models.Model):
	Myfile = models.ForeignKey('File',unique=True, related_name="file")
	Key = models.CharField(max_length=30)	
	Value = models.CharField(max_length=300)
