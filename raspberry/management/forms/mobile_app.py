from django import forms


class UploadFileForm(forms):
    title = forms.CharField(max_length=150)
    file = forms.FileField()

__author__ = 'edison7500'


