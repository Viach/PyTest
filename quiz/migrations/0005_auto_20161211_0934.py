# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20161211_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answered',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='question',
            name='wrong_answered',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
