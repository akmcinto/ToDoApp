# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-24 21:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='List',
            new_name='TodoList',
        ),
        migrations.RenameField(
            model_name='todolist',
            old_name='title',
            new_name='list_title',
        ),
    ]
