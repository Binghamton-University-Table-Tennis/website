# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-28 04:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Greeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
            ],
            options={
                'db_table': 'visits',
                'verbose_name_plural': 'Visits',
            },
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Winner_First_Name', models.CharField(max_length=20)),
                ('Winner_Last_Name', models.CharField(max_length=20)),
                ('Loser_First_Name', models.CharField(max_length=20)),
                ('Loser_Last_Name', models.CharField(max_length=20)),
                ('Winner_Score', models.IntegerField()),
                ('Loser_Score', models.IntegerField()),
                ('Day', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('Points', models.IntegerField(default=0, editable=False)),
                ('Winner_Rating', models.IntegerField(default=0, editable=False)),
                ('Loser_Rating', models.IntegerField(default=0, editable=False)),
                ('Updated', models.IntegerField(default=0, editable=False)),
            ],
            options={
                'db_table': 'matches',
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.CharField(max_length=20)),
                ('Last_Name', models.CharField(max_length=20)),
                ('Rating', models.IntegerField(default=1000, editable=False)),
                ('Matches_Won', models.IntegerField(default=0, editable=False)),
                ('Matches_Lost', models.IntegerField(default=0, editable=False)),
                ('Matches_Played', models.IntegerField(default=0, editable=False)),
                ('Win_Rate', models.IntegerField(default=0, editable=False)),
                ('Standing', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
            ],
            options={
                'db_table': 'players',
                'verbose_name_plural': 'Players',
            },
        ),
    ]
