# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-08 17:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fruit', '0001_initial'),
        ('meat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cranberry',
            name='bacon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='meat.Bacon'),
        ),
    ]