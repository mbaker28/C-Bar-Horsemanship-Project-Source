# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-08 21:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0024_auto_20160508_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidents',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='phonelog',
            name='date',
            field=models.DateField(),
        ),
    ]
