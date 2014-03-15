#coding=utf-8
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import HiddenInput, TextInput
COMPANY = u'C'
PERSONAL = u'P'
AMATEUR = u'A'
SHOP_TYPE_CHOICES = (
        (COMPANY, _('company')),
        (PERSONAL,  _('personal')),
        (AMATEUR,  _('amateur')),
    )
class GuokuPlusApplicationForm(forms.Form):
    taobao_url = forms.URLField(widget=forms.TextInput(attrs={'class':'form-control'}))
    total_volume = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}),min_value = 1, 
                                  error_messages = {'invalid' : u'数量最少为1'})
    sale_price = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control'}),min_value = 0,
                                  error_messages = {'invalid' : u'优惠价不能小于0'})
    seller_remarks = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length = 500)
    agree_tos = forms.BooleanField(widget=forms.CheckboxInput(attrs={"checked" : "checked"}))

class ShopVerificationForm(forms.Form):
    shop_type = forms.ChoiceField(widget = forms.RadioSelect(), choices = SHOP_TYPE_CHOICES )
    company_name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}),max_length = 100)
    qq_account = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}),max_length = 50)
    email = forms.EmailField(widget = forms.TextInput(attrs={'class':'form-control'}),max_length = 50)
    mobile = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}),max_length = 50)
    main_products = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}),max_length = 50)
    intro = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}),max_length = 50)
    
