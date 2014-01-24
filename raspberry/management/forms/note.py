from django import forms
from django.utils.translation import gettext_lazy as _

class NoteForms(forms.Form):
    note = forms.CharField(label=_('note'), widget=forms.Textarea(), help_text=_(''))
    weight = forms.IntegerField(label=_('weight'), help_text=_(''))

__author__ = 'edison'
