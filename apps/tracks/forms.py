from django import forms
from models import *

language_choices = (
			('bt7', 'bt7'),
			('sans', 'sans'),
			('refl', 'refl'),
			('andr', 'andr'),
			('tas', 'tas'),
)

class languageSelectForm(forms.Form):
	instruments = forms.ChoiceField(choices = language_choices)
	
class titleOnlyForm(forms.Form):
	new_project = forms.CharField(initial="My Project")
	
class titleOnlyFormExperiment(forms.Form):
	new_experiment = forms.CharField(initial="00000000")
	
class experimentForm(forms.Form):
	facility = forms.ModelChoiceField(queryset = Facility.objects.all(),empty_label="(Select a Facility)")
	instrument_class = forms.ModelChoiceField(queryset = User.objects.all(), empty_label="(Select an instrument class)") #how to generate the choices
	instrument_name = forms.ModelChoiceField(queryset= Instrument.objects.all(), empty_label="(Select an instrument)")
	templates = forms.ModelMultipleChoiceField(queryset = Template.objects.all())
	files = forms.FileField()
	
