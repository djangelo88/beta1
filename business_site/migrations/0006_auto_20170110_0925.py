# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-10 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_site', '0005_auto_20170105_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffservices',
            name='service',
            field=models.CharField(max_length=100),
        ),
    ]
