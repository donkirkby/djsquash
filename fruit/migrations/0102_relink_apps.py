# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-08 18:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0100_unlink_apps'),
        ('meat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cranberry',
            name='bacon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='meat.Bacon'),
        ),
    ]