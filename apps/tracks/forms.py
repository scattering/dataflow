from django import forms
from models import *

# language_choices should be the same as instrument_class_choices
language_choices = (
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
	facility = forms.ModelChoiceField(queryset = Facility.objects.all(),empty_label=u"\u2013")
	instrument_class = forms.ChoiceField(instrument_class_choices) #how to generate the choices
	instrument_name = forms.ModelChoiceField(queryset=Instrument.objects.all(), empty_label=u"\u2013")

class experimentForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        print 'kwargs:',kwargs
        USER = kwargs.pop('USER')
        experiment = kwargs.pop('experiment')
        super(experimentForm2, self).__init__(*args, **kwargs)
        self.fields['new_templates'] = forms.ModelMultipleChoiceField(queryset=Template.objects.filter(user=USER), label='Add templates', widget=forms.CheckboxSelectMultiple)
        self.fields['new_files'] = forms.FileField(label='Add files')
        self.fields['new_files'].widget.attrs['multiple'] = 'true'
        print experiment.templates.all()
        self.fields['cur_templates'] = forms.ModelMultipleChoiceField(queryset=experiment.templates.all(), label='Current templates', widget=forms.CheckboxSelectMultiple)
        self.fields['cur_files'] = forms.ModelMultipleChoiceField(queryset=experiment.Files.all(), label='Current files', widget=forms.CheckboxSelectMultiple)
