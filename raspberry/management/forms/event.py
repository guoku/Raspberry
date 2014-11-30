from django import forms
from django.utils.translation import gettext_lazy as _

class BaseEventFomr(forms.Form):

    tag = forms.CharField(
        label=_('tag'),
        widget=forms.TextInput(attrs={'class':'form-control'})
    )


__author__ = 'edison'
