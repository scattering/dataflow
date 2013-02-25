from django.contrib import admin

from models import Project
from models import Experiment

#NOTE: class not used currently...
class ProjectAdmin(admin.ModelAdmin):
    exclude = ('templateInstances',)
    
#admin.site.register(Project, ProjectAdmin)

admin.site.register(Project)
admin.site.register(Experiment)