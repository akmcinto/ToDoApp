from django.forms import ModelForm
from .models import Item, TodoList

class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item_text']

class NewListForm(ModelForm):
    class Meta:
        model = TodoList
        fields = ['list_title']
