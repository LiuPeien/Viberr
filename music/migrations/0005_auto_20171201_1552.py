# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-01 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20171201_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stopwords',
            name='word',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]