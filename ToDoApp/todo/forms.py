from django import forms

class NewItemForm(forms.Form):
    new_item = forms.CharField(max_length=250)
