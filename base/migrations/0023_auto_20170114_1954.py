# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-14 19:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20170114_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 14, 19, 54, 49, 410928)),
        ),
    ]
