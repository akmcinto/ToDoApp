from django import forms
from .models import Item, TodoList

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_text']

class NewListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['list_title', 'creation_date']
