#coding=utf-8
from django import forms
from django.utils.translation import gettext_lazy as _

from datetime import date

APPROVE = u"approve"
REJECT = u"reject"
ACTION_CHOICES = (
    (APPROVE, _('approve')),
    (REJECT, _('reject')),
    )
class GuokuPlusActivityForm(forms.Form):
    app_id = forms.CharField(max_length = 32, widget = forms.HiddenInput())
    action = forms.ChoiceField(widget = forms.Select(), choices = ACTION_CHOICES)
    editor_remarks = forms.CharField(max_length = 120)
    start_time = forms.DateField(widget = forms.DateInput(attrs={'id' : 'dateinput', 'readonly' : 'readonly'}), required=False)

    def clean_start_time(self):
        if self.cleaned_data.get('start_time') == None:
            return None
        if self.cleaned_data['start_time'] <= date.today():
            raise forms.ValidationError("时间必须大于" + str(date.today()))
        return self.cleaned_data['start_time']
