# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-20 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0010_auto_20160320_0523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.CharField(default=None, max_length=128),
        ),
    ]
