# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-02 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_auto_20171201_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classifier',
            name='classifier_name',
            field=models.CharField(max_length=50),
        ),
    ]
