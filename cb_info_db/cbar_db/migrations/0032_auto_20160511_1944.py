# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-12 00:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0031_auto_20160511_1944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpermission',
            options={'permissions': ('test_admin', 'Admin')},
        ),
    ]
