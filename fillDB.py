from apps.tracks.models import *
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
    
if len(Instrument.objects.all()) < 1:
        Instrument.objects.create(Name='TripleAxis', instrument_class='tas')
        Instrument.objects.create(Name='ng3', instrument_class='sans')
        Instrument.objects.create(Name='ANDR', instrument_class='andr')
        Instrument.objects.create(Name='andr2', instrument_class='andr2')
        Instrument.objects.create(Name='asterix', instrument_class='asterix')
        Instrument.objects.create(Name='NCNR PBR', instrument_class='refl')

if len(Facility.objects.all()) < 1:
        Facility.objects.create(Name='NCNR')
        Facility.objects.create(Name='HFIR')
        Facility.objects.create(Name='Chalk River')
        
# There is probably a better way to set the default domain and name.
if Site._meta.installed:
        mysite = Site.objects.get_current()
else:
        mysite = RequestSite(request)
if mysite.domain == '':
        mysite.domain = 'drneutron.org'
        mysite.save()
if mysite.name == '':
        mysite.name = 'drneutron.org'
        mysite.save()
        
#if len(Template.objects.all()) == 0:
#        temp = Template.objects.create(Title='testTemplate')
#        temp.metadata.add(User.objects.get(id=1))

#to add a new model (instrument, facility, or template) manually, you can run:    
        # python manage.py shell
        # then, as done above... 
        # from apps.tracks.models import *
        # MODEL_NAME_HERE.objects.create(params) 
