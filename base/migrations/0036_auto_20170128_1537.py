# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-28 15:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_auto_20170127_0411'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='name',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 28, 15, 37, 49, 367426)),
        ),
    ]