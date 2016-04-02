# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-02 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0009_converted_yes_no_fields_in_medicalinfo_to_boolean_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiabilityRelease',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('signature', models.CharField(max_length=75)),
                ('participant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbar_db.Participant')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='liabilityrelease',
            unique_together=set([('participant_id', 'date')]),
        ),
    ]
