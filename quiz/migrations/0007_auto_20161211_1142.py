# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20161211_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answered',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='question',
            name='wrong_answered',
            field=models.IntegerField(default=1),
        ),
    ]
