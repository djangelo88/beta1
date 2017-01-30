# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-28 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_site', '0006_auto_20170110_0925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='websitecontrol',
            name='website',
        ),
        migrations.AddField(
            model_name='website',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='WebsiteControl',
        ),
    ]
