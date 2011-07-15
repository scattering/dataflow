from django import forms

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
	title = forms.CharField(initial="My Project")
	
#class experimentForm(forms.Form):
	
