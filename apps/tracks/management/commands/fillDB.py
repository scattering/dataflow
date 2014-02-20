from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = ''
    help = "Initializes the tracks database."

    def handle(self, *args, **options):
        set_instruments()
        set_domain()

FACILITIES = {
    'NCNR': {
        'ncnr.tas': dict(bt4='BT-4', bt7='BT-7', macs='MACS', ng5='spins'),
        'ncnr.refl': dict(ngd='PBR', cgd='Magik', ng7='NG-7',
                          ng1='NG-1', cg1='AND/R', # Old instruments
        ),
        'ncnr.ospec': dict(ngd='PBR offspecular', cgd='Magik offspecular',
                          ng1='NG-1 offspecular', cg1='AND/R offspecular', # Old instruments
        ),
        'ncnr.sans': dict(ng3sans='NG-3 SANS', ng7sans='NG-7 SANS',
                          ngbsans='NG-B SANS'),
    },
    #'HFIR':{},
    #'Chalk River': {},
    'LANSCE': {
        'lansce.ospec.asterix': dict(asterix='Asterix'),
    },
}

def set_instruments():
    from apps.tracks.models import Instrument, Facility

    for facility_name,instrument_group in FACILITIES.items():
        facility = Facility.objects.create(name=facility_name)
        for type,instruments in instrument_group.items():
            for beamline,name in instruments.items():
                Instrument.objects.create(name=name, type=type,
                                          facility=facility,
                                          beamline=beamline)
    # Need to plug in initial templates and calibration files

def set_domain():
    from django.contrib.sites.models import RequestSite
    from django.contrib.sites.models import Site
    from django.conf import settings

    site = Site.objects.get_current()
    site.domain = settings.SITE_DOMAIN
    site.name = settings.SITE_NAME
    site.save()

#if len(Template.objects.all()) == 0:
#        temp = Template.objects.create(Title='testTemplate')
#        temp.metadata.add(User.objects.get(id=1))

#to add a new model (instrument, facility, or template) manually, you can run:
        # python manage.py shell
        # then, as done above...
        # from apps.tracks.models import *
        # MODEL_NAME_HERE.objects.create(params)
