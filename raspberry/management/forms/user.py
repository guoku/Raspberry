# coding=utf8
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class UserForms(forms.Form):

    Man = u'M'
    Woman = u'F'
    Other = u'O'
    GENDER_CHOICES = (
        (Man, u'男'),
        (Woman,  u'女'),
        (Other,  u'其他')
    )

    username = forms.CharField(max_length = 30, widget = forms.TextInput(attrs = {'class' : 'input-xxlarge'}), label = _('username'), help_text = _(''))
    nickname = forms.CharField(max_length = 30, widget = forms.TextInput(attrs = {'class':'input-xxlarge'}), label = _('nickname'), help_text = _(''))
    email = forms.EmailField(widget = forms.TextInput(attrs = {'class' : 'input-xxlarge'}), label = _('email'), help_text = _(''))
    gender = forms.ChoiceField(choices = GENDER_CHOICES, label = _('gender'), help_text = _(''))
    bio = forms.CharField(required = False, widget=forms.Textarea(attrs={'class' : 'input-xxlarge', 'rows' : '3'}),
                          label = _('bio'), help_text = _(''))
    website = forms.URLField(required = False, widget = forms.TextInput(attrs = {'class' : 'input-xxlarge'}), label = _('website'), help_text = _(''))


    # def clean_email(self):
    #     _email = self.cleaned_data.get('email', None)
    #     try:
    #         User.objects.get(email=_email)
    #     except User.DoesNotExist:
    #         return _email
    #     raise forms.ValidationError(self.error_messages['duplicate_email'])

__author__ = 'edison'
