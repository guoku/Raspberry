from django import forms
from django.utils.translation import gettext_lazy as _

class ShareFrom(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label=_(''), help_text=_(''), initial=_('shared content'))

__author__ = 'edison7500'
