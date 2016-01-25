from django import forms

class NewItemForm(forms.Form):
    new_item = forms.CharField(label='New item', max_length=250)
