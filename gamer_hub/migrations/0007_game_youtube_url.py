# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-22 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamer_hub', '0006_merge_20180322_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='youtube_url',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
