# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-04 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbar_db', '0016_add_date_field_to_donation_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='evalridingexercises',
            name='basic_control_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='basic_seat_english_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='basic_seat_western_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='basic_trail_rules_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_control_horse_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_control_horse_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_control_horse_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_control_horse_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_halt_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_halt_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_halt_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_halt_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_post_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_post_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_post_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_post_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_steer_over_cavalletti_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_steer_over_cavalletti_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_steer_over_cavalletti_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='can_steer_over_cavalletti_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='circle_at_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='circle_at_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='circle_at_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='circle_canter_no_stirrups_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='circle_trot_no_stirrups_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='dismount_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='drop_pickup_stirrups_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='drop_pickup_stirrups_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='drop_pickup_stirrups_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='drop_pickup_stirrups_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='emergency_dismount_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='four_natural_aids_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='hand_pos_english_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='hand_post_western_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='holds_handhold_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='holds_handhold_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='holds_handhold_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='holds_handhold_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='holds_reins_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='holds_reins_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='holds_reins_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='holds_reins_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='jump_crossbar_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='jump_crossbar_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='jump_crossbar_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='jump_crossbar_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='maintain_half_seat_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='maintain_half_seat_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='maintain_half_seat_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='maintain_half_seat_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='mount_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='never_ridden_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='proper_diagonal_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='proper_diagonal_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='proper_diagonal_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='proper_diagonal_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='proper_lead_canter_knows_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='proper_lead_canter_sees_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='reverse_at_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='reverse_at_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='rides_no_stirrups_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='rides_no_stirrups_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='rides_no_stirrups_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='rides_no_stirrups_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='seat_at_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='seat_at_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='seat_at_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='shorten_lengthen_reins_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='shorten_lengthen_reins_post_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='shorten_lengthen_reins_sit_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='shorten_lengthen_reins_walk_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='two_point_canter_com',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='evalridingexercises',
            name='two_point_trot_com',
            field=models.CharField(max_length=100, null=True),
        ),
    ]