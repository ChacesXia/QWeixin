# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_auto_20160629_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weixininfo',
            name='weixinid',
            field=models.CharField(max_length=200, verbose_name='微信号'),
        ),
    ]
