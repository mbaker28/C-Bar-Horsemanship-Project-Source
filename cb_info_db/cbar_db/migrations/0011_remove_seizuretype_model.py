# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-01 16:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0010_add_type_of_seizure_field_to_seizureeval_model'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='seizuretype',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='seizuretype',
            name='seizure_eval',
        ),
        migrations.DeleteModel(
            name='SeizureType',
        ),
    ]