# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
