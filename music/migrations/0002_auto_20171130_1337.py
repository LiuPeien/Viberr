# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-30 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifier',
            name='classifier_labels',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='classifier',
            name='classifier_name',
            field=models.CharField(max_length=50),
        ),
    ]
