from django import forms
from .utils import composa_opcions_grups

class descarregaAlumnesForm(forms.Form):
    grups = forms.CharField(label="Alumnes",
        widget=forms.SelectMultiple(
                choices=composa_opcions_grups()
        ))