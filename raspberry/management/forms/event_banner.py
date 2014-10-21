from django import forms
from django.utils.translation import gettext_lazy as _

class CreateEventBannerForms(forms.Form):

    link = forms.URLField(
        label=_('link'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )
    event_banner_image = forms.FileField(
        label=_('event banner image'),
        widget=forms.FileInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )

    def save(self):

        pass

__author__ = 'edison'
