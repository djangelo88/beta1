# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-14 16:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_auto_20170114_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Address'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 14, 16, 14, 58, 130654)),
        ),
    ]