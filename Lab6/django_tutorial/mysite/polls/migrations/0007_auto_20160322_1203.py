# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20160322_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='lati',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='choice',
            name='long',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='lati',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='long',
            field=models.FloatField(default=0),
        ),
    ]
