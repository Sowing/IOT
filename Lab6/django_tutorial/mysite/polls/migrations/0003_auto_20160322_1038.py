# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_remove_choice_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='lati',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='loc',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='long',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='weather',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
