from django.db import models
from django.contrib.auth.models import User, Permission

# Create your models here.

class Test(models.Model):
	field1 = models.CharField(max_length=200)
	field2 = models.IntegerField(null=True)
	def __unicode__(self):
		return self.field1

# class User     is provided by contrib.auth

class Userprofile(models.Model):
	userdisplay = models.CharField(max_length=300)

# class Permission     is provided by contrib.auth

class File(models.Model):
	permissions = models.ForeignKey(Permission, null=True) # or should this be a string of permission names
	name = models.CharField(max_length=160, primary_key=True) # what format are we storing the contents in?
	location = models.CharField(max_length=300) #location of file on disc
	metadata = models.ManyToManyField('Metadata', null=True)
	def __unicode__(self):
		return self.location.split('/')[-1]
	
class Metadata(models.Model):
	Myfile = models.ForeignKey('File',unique=True, related_name="file", null=True)
	Key = models.CharField(max_length=30)	
	Value = models.CharField(max_length=300)
	def __unicode__(self):
		return self.Key + ": " + self.Value

class Template(models.Model):
	Title = models.CharField(max_length=50) # name of experiment associated with template
	Representation = models.CharField(max_length= 5000) # can easily convert back and forth from strings to 							    # dicts with str(dict) and dict(str)
							    # might want to encode these representations, as they're
							    # pretty long
	user = models.ForeignKey(User, unique=True, null=True)
	permissions = models.ForeignKey(Permission, null=True)

class Project(models.Model):
	Title = models.CharField(max_length=50) 
	user = models.ForeignKey(User, unique=True, null=True)
	permissions = models.ForeignKey(Permission, null=True)
	experiments = models.ManyToManyField('Experiment', null=True)
	templateInstances = models.ManyToManyField('Template', null=True) # are the templates here and  								          # under Instruments meant to be different

class Experiment(models.Model):
	ProposalNum = models.IntegerField(null=True) # IMS proposal/request number
	Files = models.ForeignKey('File', null=True)
	users = models.ForeignKey(User, null=True)
	permissions = models.ForeignKey(Permission, null=True)
	instrument = models.ForeignKey('Instrument', unique=True, null=True)

class Instrument(models.Model):
	Name = models.CharField(max_length=50) #e.g., TAS, bt7, SANS
	Templates = models.ForeignKey('Template', null=True)
	metadata = models.ForeignKey('Metadata', null=True)
	Calibrations = models.CharField(max_length=100) # is this so that we can have different instances of an
							# an instrument varying by calibration?
	
	
	
	
	
	


