# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeixinInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weixinid', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('originid', models.CharField(max_length=200)),
                ('appid', models.CharField(max_length=200)),
                ('appkey', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='test',
        ),
    ]
