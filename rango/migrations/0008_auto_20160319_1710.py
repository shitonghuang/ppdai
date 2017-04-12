# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 17:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0007_auto_20160319_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='author',
            field=models.CharField(default=None, max_length=128),
        ),
        migrations.AddField(
            model_name='page',
            name='content',
            field=models.CharField(default=None, max_length=600),
        ),
        migrations.AddField(
            model_name='page',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='page',
            name='sourcefile',
            field=models.FilePathField(default='', path='profile_file'),
        ),
        migrations.AddField(
            model_name='page',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='page',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.URLField(default=''),
        ),
    ]