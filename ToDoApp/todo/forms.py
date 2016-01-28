from django.forms import ModelForm, Form, BooleanField
from django.contrib.auth.models import User
from .models import Item, TodoList

class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item_text']

class NewListForm(ModelForm):
    class Meta:
        model = TodoList
        fields = ['list_title']
