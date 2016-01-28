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

from django.contrib import admin
from .models import TodoList, Item

class ItemInline(admin.TabularInline):
    model = Item
    extra = 3

class ListAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['list_title', 'list_user']}),
                ]
    inlines = [ItemInline]
    list_filter = ['list_title']
    search_fields = ['list_title']

    # vikingosegundo, http://stackoverflow.com/questions/1477319/in-django-how-do-i-know-the-currently-logged-in-user, 2016-01-26
    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance,'created_by'):
            instance.list_user = request.user
        instance.save()
        form.save_m2m()
        return instance

    def save_formset(self, request, form, formset, change):

        def set_user(instance):
            if not instance.list_user:
                instance.list_user = request.user
            instance.save()

        if formset.model == TodoList:
            instances = formset.save(commit=False)
            map(set_user, instances)
            formset.save_m2m()
            return instances
        else:
            return formset.save()

admin.site.register(TodoList, ListAdmin)
