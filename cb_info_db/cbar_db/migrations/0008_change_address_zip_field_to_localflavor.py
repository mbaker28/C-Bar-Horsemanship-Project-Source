# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-21 15:47
from __future__ import unicode_literals

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0007_change_phone_fields_to_localflavor_phone_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='address_zip',
            field=localflavor.us.models.USZipCodeField(max_length=10),
        ),
    ]