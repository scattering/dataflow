from django import forms

language_choices = (
			('bt7', 'bt7'),
			('sans', 'sans'),
			('refl', 'refl'),
			('andr', 'andr')
)

class languageSelectForm(forms.Form):
	instruments = forms.ChoiceField(choices = language_choices)
