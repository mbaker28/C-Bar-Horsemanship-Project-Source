# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-07 04:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0020_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evalattitude',
            name='general_attitude_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='general_attitude_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='general_attitude_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='looking_at_horses_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='looking_at_horses_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='looking_at_horses_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='mounting_after_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='mounting_after_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='mounting_after_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='mounting_before_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='mounting_before_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='mounting_before_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='participates_exercises_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='participates_exercises_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='participates_exercises_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='participates_games_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='participates_games_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='participates_games_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='petting_horses_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='petting_horses_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='petting_horses_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='riding_after_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='riding_after_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='riding_after_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='riding_before_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='riding_before_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='riding_before_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='riding_during_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='riding_during_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='riding_during_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='understands_directions_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='understands_directions_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='understands_directions_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='up_down_ramp_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='up_down_ramp_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='up_down_ramp_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='walking_through_barn_appearance',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='walking_through_barn_motivated',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='evalattitude',
            name='walking_through_barn_willing',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('-', 'N/A')], default='-', max_length=1),
        ),
    ]