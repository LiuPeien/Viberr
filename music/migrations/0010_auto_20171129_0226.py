# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-29 02:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classy', '0009_classifier_corpus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classifier',
            name='user',
        ),
        migrations.RemoveField(
            model_name='corpus',
            name='classifier',
        ),
        migrations.DeleteModel(
            name='Classifier',
        ),
        migrations.DeleteModel(
            name='Corpus',
        ),
    ]
