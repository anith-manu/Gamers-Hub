# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-21 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamer_hub', '0004_auto_20180321_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_info',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='game',
            name='picture',
            field=models.ImageField(blank=True, upload_to='game_covers'),
        ),
        migrations.AddField(
            model_name='game',
            name='publisher',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.CharField(max_length=800),
        ),
    ]