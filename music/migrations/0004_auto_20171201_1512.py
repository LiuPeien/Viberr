# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-01 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_stopwords'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stopwords',
            old_name='Stopwords_word',
            new_name='word',
        ),
    ]