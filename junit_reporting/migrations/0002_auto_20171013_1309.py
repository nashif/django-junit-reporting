# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('junit_reporting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='junitreport',
            name='build_number',
            field=models.IntegerField(unique=True),
        ),
    ]
