# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-30 22:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0005_removed_unneeded_fk_from_medicalinfo_table_and_changed_pk_of_medication_table_1_of_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='participant_id',
        ),
    ]