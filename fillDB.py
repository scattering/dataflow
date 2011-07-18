from apps.tracks.models import *
if len(Instrument.objects.all()) < 1:
	Instrument.objects.create(Name='bt7',instrument_class = 'tas')
	Instrument.objects.create(Name='ng3',instrument_class = 'sans')
if len(Facility.objects.all()) == 0:
	Facility.objects.create(Name='NCNR')
if len(Template.objects.all()) == 0:
	Template.objects.create(Title='testTemplate', user = User.objects.get(id=1))

