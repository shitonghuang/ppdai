# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-04-09 10:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0015_loan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='lisitngid',
            new_name='listingid',
        ),
    ]
