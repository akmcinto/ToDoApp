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

import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class TodoList(models.Model):
    list_title = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created', default=datetime.datetime.now())
    list_user = models.ForeignKey(User)

    def __str__(self):
        return self.list_title

class Item(models.Model):
    item_text = models.CharField(max_length=250)
    creation_date = models.DateTimeField('date created', default=datetime.datetime.now())
    completed = models.BooleanField(default=False)
    todo_list = models.ForeignKey(TodoList)

    def __str__(self):
        return self.item_text

    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Item.objects.get(pk=self.pk)
            if orig.completed != self.completed:
                print ('completed changed')
        super(Item, self).save(*args, **kw)
