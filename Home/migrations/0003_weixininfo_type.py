# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_auto_20160629_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='weixininfo',
            name='type',
            field=models.CharField(default='0', max_length=2),
        ),
    ]
