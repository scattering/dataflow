from django.db import models
from django.contrib.auth.models import User #, Permission

# Create your models here.

class Test(models.Model):
    field1 = models.CharField(max_length=200)
    field2 = models.IntegerField(null=True)
    def __unicode__(self):
        return self.field1

# class User     is provided by contrib.auth

class Userprofile(models.Model):
    user = models.ForeignKey(User)
    userdisplay = models.CharField(max_length=300)

# class Permission     is provided by contrib.auth

class File(models.Model):
    #permissions = models.ForeignKey(Permission, null=True) # or should this be a string of permission names
    name = models.CharField(max_length=160, primary_key=True) # sha1 hash of file contents
    friendly_name = models.CharField(max_length=60)
    location = models.CharField(max_length=300) #location of file on disk
    metadata = models.ManyToManyField('Metadata', null=True)
    def __unicode__(self):
        return self.friendly_name

class Metadata(models.Model):
    Myfile = models.ForeignKey('File', related_name="file")
    Key = models.CharField(max_length=30)	
    Value = models.CharField(max_length=300)
    def __unicode__(self):
        return self.Key + ": " + self.Value

class Template(models.Model):
    Title = models.CharField(max_length=50)
    Representation = models.TextField() # can easily convert back and forth from strings to dicts with str(dict) and dict(str)
    user = models.ForeignKey(User)
    #permissions = models.ForeignKey(Permission, null=True)
    def __unicode__(self):
        return self.Title

class Project(models.Model):
    Title = models.CharField(max_length=50) 
    user = models.ForeignKey(User)
    #permissions = models.ForeignKey(Permission, null=True)
    experiments = models.ManyToManyField('Experiment', null=True)
    templateInstances = models.ManyToManyField('Template', null=True) # are the templates here and  								          # under Instruments meant to be different

    def __unicode__(self):
        return self.Title

class Experiment(models.Model):
    ProposalNum = models.CharField(max_length=100) # IMS proposal/request number
    Files = models.ManyToManyField('File', null=True)
    Results = models.ManyToManyField('Result', null=True)
    facility = models.ForeignKey('Facility', null=True)
    users = models.ForeignKey(User)
    #permissions = models.ForeignKey(Permission, null=True)
    instrument = models.ForeignKey('Instrument', null=True)
    templates = models.ManyToManyField('Template', null=True)
    def __unicode__(self):
        return self.ProposalNum

class Instrument(models.Model):
    Name = models.CharField(max_length=50) #e.g. bt7 
    Templates = models.ManyToManyField('Template', null=True)
    metadata = models.ManyToManyField('Metadata', null=True)
    instrument_class = models.CharField(max_length=50)
    Calibrations = models.CharField(max_length=100) # is this so that we can have different instances of an
                            # an instrument varying by calibration?

    def __unicode__(self):
        return self.Name

class Facility(models.Model):
    Name = models.CharField(max_length=50) #e.g., NCNR, HFIR, 
    instruments = models.ManyToManyField('Instrument', null=True)
    def __unicode__(self):
        return self.Name

class Result(models.Model):
    name = models.CharField(max_length=160, primary_key=True) # sha1 hash of template
    template_representation = models.TextField() # template that created the result
    Title = models.CharField(max_length=50)
    location = models.CharField(max_length=300) #location of file on disk
    metadata = models.ManyToManyField('Metadata', null=True)
    def __unicode__(self):
        return self.Title





