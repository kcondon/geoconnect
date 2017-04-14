# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-14 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gis_basic_file', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gisdatafile',
            name='datafile_is_restricted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='gisdatafile',
            name='dataset_citation',
            field=models.TextField(),
        ),
    ]
