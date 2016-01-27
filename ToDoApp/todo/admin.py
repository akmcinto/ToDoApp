from django.contrib import admin
from .models import TodoList, Item

class ItemInline(admin.TabularInline):
    model = Item
    extra = 3

class ListAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['list_title']}),
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
