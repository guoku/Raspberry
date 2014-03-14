#coding=utf-8
from django import forms
from django.forms.widgets import HiddenInput, TextInput
class GuokuPlusApplicationForm(forms.Form):
    taobao_url = forms.URLField()
    total_volume = forms.IntegerField(min_value = 1, 
                                  error_messages = {'invalid' : u'数量最少为1'})
    sale_price = forms.FloatField(min_value = 0,
                                  error_messages = {'invalid' : u'优惠价不能小于0'})
    seller_remarks = forms.CharField(max_length = 500)
    agree_tos = forms.BooleanField(widget=forms.CheckboxInput(attrs={"checked" : "checked"}))
class ShopVerificationForm(forms.Form):
    shop_type = forms.ChoiceField(widget = forms.RadioSelect(), choices = [u'公司',u'个体', u'业余'] )
    company_name = forms.CharField(max_length = 100)
    qq_account = forms.CharField(max_length = 50)
    email = forms.EmailField(max_length = 50)
    mobile = forms.CharField(max_length = 50)
    main_products = forms.CharField(max_length = 50)
    intro = forms.CharField(max_length = 50)
    
