# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-06 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0022_renamed_gait_standing_down_field_to_gait_sitting_down_in_adaptionsneeded_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_balance',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_decline',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_flat',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_incline',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_sitting_down',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_stairs',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_standing_up',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_straddle_down',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_straddle_up',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationsneeded',
            name='gait_uneven',
            field=models.CharField(choices=[('I', 'Independent'), ('M', 'Minimal asst.'), ('F', 'Full asst.'), ('N', 'n/a')], default='N', max_length=1, null=True),
        ),
    ]
