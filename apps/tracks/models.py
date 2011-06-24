from django.db import models

# Create your models here.

class Test(models.Model):
	field1 = models.CharField(max_length=200)
	field2 = models.IntegerField()
	def __unicode__(self):
		return self.field1
