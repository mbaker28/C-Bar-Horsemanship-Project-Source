# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-12 00:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0028_add_time_field_increase_description_max_length_and_set_pk_to_date+time+participant_id_in_incidents_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authorizeduser',
            options={'permissions': ('admin', 'Admin')},
        ),
    ]
