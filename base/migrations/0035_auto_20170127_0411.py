# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-27 04:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_auto_20170123_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 27, 4, 11, 25, 829536)),
        ),
    ]
