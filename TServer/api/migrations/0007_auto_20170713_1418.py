# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-13 05:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_star_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
