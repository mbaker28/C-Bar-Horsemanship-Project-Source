# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-06 01:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0015_added_signature_field_to_seizureeval_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seizureeval',
            name='duration_of_last_seizure',
            field=models.CharField(max_length=100),
        ),
    ]
