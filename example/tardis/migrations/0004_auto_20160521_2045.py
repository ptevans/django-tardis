# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-21 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tardis', '0003_auto_20160521_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetravel',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timetravel',
            name='started',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='timetravel',
            name='step_size',
            field=models.IntegerField(help_text='Step size in minutes. The Tardis will take us to our destination stopping at intervals to execute any callbacksthat are defined for our trips.'),
        ),
    ]