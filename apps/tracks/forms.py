from django import forms
from models import *

# language_choices should be the same as instrument_class_choices
language_choices = (
			('bt7', 'bt7'),
			('sans', 'sans'),
			('refl', 'refl'),
			('andr', 'andr'),
			('tas', 'tas'),
			('andr2', 'andr2'),
)

instrument_class_list = []
for i in Instrument.objects.all():
	ins_class = str(i.instrument_class)
	if not instrument_class_list.count(ins_class):
		instrument_class_list.append(tuple([ins_class, ins_class]))
instrument_class_choices = tuple(instrument_class_list)

class languageSelectForm(forms.Form):
	instruments = forms.ChoiceField(choices = language_choices)
	
class titleOnlyForm(forms.Form):
	new_project = forms.CharField(initial="My Project")
	
class titleOnlyFormExperiment(forms.Form):
	new_experiment = forms.CharField(initial="00000000")
	
##### REMOVE THE BLANK=TRUE
class experimentForm1(forms.Form):
	facility = forms.ModelChoiceField(queryset = Facility.objects.all(),empty_label="(Select a Facility)")
	instrument_class = forms.ChoiceField(instrument_class_choices) #how to generate the choices
	instrument_name = forms.ModelChoiceField(queryset= Instrument.objects.all(), empty_label="(Select an instrument)")

class experimentForm2(forms.Form):

  	def __init__(self, *args, **kwargs):
    		USER = kwargs.pop('USER')
    		super(experimentForm2, self).__init__(*args, **kwargs)
		self.fields['templates'] = forms.ModelChoiceField(queryset = Template.objects.filter(user=USER), empty_label="(Select a Template)")
		self.fields['files'] = forms.FileField()
