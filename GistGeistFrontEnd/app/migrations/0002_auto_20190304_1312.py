# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-03-04 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='author',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='poll',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]
