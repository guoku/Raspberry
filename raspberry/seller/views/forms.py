#coding=utf-8
from django import forms
from django.forms.widgets import HiddenInput
class GuokuPlusApplicationForm(forms.Form):
    taobao_item_id = forms.CharField(max_length = 20, widget = HiddenInput())
    quantity = forms.IntegerField(min_value = 1,
                                  error_messages = {                                               'invalid' : u'数量最少为1'})
    original_price = forms.FloatField(min_value = 0,
                                      error_messages = {
                                                        'invalid' : u'价格不能小于0' })
    sale_price = forms.FloatField(min_value = 0,
                                  error_messages = {                                                   'invalid' : u'优惠价不能小于0'})
    duration = forms.IntegerField(min_value = 0,
                                  error_messages = { 'invalid' : u'活动时间长度不能小于0'})

    def clean_sale_price(self):
        data = self.cleaned_data['sale_price']
        if data > self.cleaned_data['original_price']:
            raise forms.ValidationError(u'优惠价不能大于原价')
        return data
       
