# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-11 20:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20170110_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('siglas', models.CharField(default='', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=350)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=350)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Business')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min', models.IntegerField()),
                ('max', models.IntegerField()),
                ('price', models.FloatField(default=0.0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Ingredients')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=350)),
                ('tarifa_horaria', models.CharField(max_length=250)),
                ('bussines', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Business')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceWorkers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Service')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Position')),
            ],
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2017, 1, 11, 20, 1, 56, 383862)),
        ),
        migrations.AddField(
            model_name='serviceworkers',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Worker'),
        ),
        migrations.AddField(
            model_name='product',
            name='recipe',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.Recipe'),
        ),
        migrations.AddField(
            model_name='ingredients',
            name='measure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Measure'),
        ),
    ]