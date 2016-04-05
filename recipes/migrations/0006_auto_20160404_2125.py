# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-04 20:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_mealcategory_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meal',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='mealcategory',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='meal',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
