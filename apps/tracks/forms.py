from django import forms

language_choices = (
			('bt7', 'bt7'),
			('sans', 'sans'),
			('refl', 'refl'),
)

class languageSelectForm(forms.Form):
	instruments = forms.ChoiceField(choices = language_choices)
