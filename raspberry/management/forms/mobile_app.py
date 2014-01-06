from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=150, required=False)
    file = forms.FileField()

__author__ = 'edison7500'


