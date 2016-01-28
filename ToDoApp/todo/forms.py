"""
   Copyright 2016 Andrea McIntosh

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 """

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
