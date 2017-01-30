# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-02 22:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20170102_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='denied_by_system',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 2, 17, 40, 17, 799090)),
        ),
    ]
