# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-12 00:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0029_auto_20160511_1937'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authorizeduser',
            options={'permissions': 'admin'},
        ),
    ]