# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-30 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0035_auto_20170329_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practices',
            name='Date',
            field=models.DateField(editable=False),
        ),
    ]