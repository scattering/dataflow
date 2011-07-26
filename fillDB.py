from apps.tracks.models import *
if len(Instrument.objects.all()) < 1:
	Instrument.objects.create(Name='bt7', instrument_class='tas')
	Instrument.objects.create(Name='ng3', instrument_class='sans')
	Instrument.objects.create(Name='ANDR', instrument_class='andr')
	
if len(Facility.objects.all()) == 0:
	Facility.objects.create(Name='NCNR')
if len(Template.objects.all()) == 0:
	Template.objects.create(Title='testTemplate', user=User.objects.get(id=1))


#to add a new instrument, facility, template manually, you can:    
	# run python manage.py shell
	# then, as done above... 
	# from apps.tracks.models import *
	# MODEL_NAME.objects.create(params) 
