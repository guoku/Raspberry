# coding=utf-8

from django import forms


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=150, required=False)
    file = forms.FileField(
        label='选取一个 apk',
        help_text='10M 以内',
    )

__author__ = 'edison7500'


