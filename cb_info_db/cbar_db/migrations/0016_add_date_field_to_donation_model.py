# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-02 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0015_add_purpose_charfield_to_donation_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
