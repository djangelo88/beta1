# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-13 16:09
from __future__ import unicode_literals

import base.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20170112_1959'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_line', models.CharField(max_length=150)),
                ('second_line', models.CharField(max_length=150, null=True)),
                ('zip', models.IntegerField()),
            ],
            bases=(models.Model, base.models.ModelSerialize),
        ),
        migrations.CreateModel(
            name='N_City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='N_Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='N_State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.N_Country')),
            ],
        ),
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 13, 16, 9, 56, 989493)),
        ),
        migrations.AddField(
            model_name='n_city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.N_State'),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.N_City'),
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.Customer'),
        ),
    ]
