#coding=utf-8
from django import forms
from django.forms.widgets import HiddenInput, TextInput
class GuokuPlusApplicationForm(forms.Form):
    taobao_item_id = forms.CharField(max_length = 20, widget = HiddenInput())
    quantity = forms.IntegerField(min_value = 1, 
                                  error_messages = {'invalid' : u'数量最少为1'})
    original_price = forms.FloatField(min_value = 0, widget = TextInput(attrs={'readonly' :"readonly"}),
                                      error_messages = {'invalid' : u'价格不能小于0' })
    sale_price = forms.FloatField(min_value = 0,
                                  error_messages = {'invalid' : u'优惠价不能小于0'})
    remarks = forms.CharField(max_length = 500)
    def clean_sale_price(self):
        data = self.cleaned_data['sale_price']
        if data > self.cleaned_data['original_price']:
            raise forms.ValidationError(u'优惠价不能大于原价')
        return data

class ShopVerificationForm(forms.Form):
    shop_type = forms.ChoiceField(widge = forms.RadioSelect(), choices = ['公司','个体','业余'])
    company_name = forms.CharField(max_length = 100)
    qq_account = forms.CharField(max_length = 50)
    email = forms.EmailField(max_length = 50)
    mobile = forms.CharField(max_length = 50)
    main_products = forms.CharField(max_length = 50)
    intro = forms.CharField(max_length = 50)
    
