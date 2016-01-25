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

admin.site.register(TodoList, ListAdmin)
