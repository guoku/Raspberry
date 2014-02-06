from django import forms

class GuokuPlusApplicationForm(forms.Form):
    taobao_item_id = forms.CharField(max_length = 20)
    quantity = forms.IntegerField(min_value = 1)
    original_price = forms.FloatField()
    sale_price = forms.FloatField()
    duration = forms.IntegerField()
  
     
