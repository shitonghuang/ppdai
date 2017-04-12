# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-04-09 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0017_auto_20170409_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('amount', models.IntegerField(default=0)),
                ('rate', models.IntegerField(default=0)),
                ('charge', models.IntegerField(default=0)),
            ],
        ),
    ]
