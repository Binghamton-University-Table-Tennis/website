# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-27 16:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0016_auto_20170325_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='EBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Position', models.IntegerField(choices=[(1, b'President'), (2, b'Co-President'), (3, b'Treasurer'), (4, b'Secretary'), (5, b'Webmaster')])),
            ],
            options={
                'db_table': 'eboard',
                'verbose_name_plural': 'EBoard',
            },
        ),
        migrations.AlterField(
            model_name='players',
            name='LastSeen',
            field=models.DateField(default=datetime.date(2017, 3, 27), editable=False),
        ),
    ]