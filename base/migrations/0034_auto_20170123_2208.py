# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-23 22:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_auto_20170118_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.CharField(default=0, max_length=350),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 23, 22, 8, 32, 111172)),
        ),
    ]
