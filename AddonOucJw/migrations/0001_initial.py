# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Home', '0008_auto_20160630_0737'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coursename', models.CharField(max_length=200, verbose_name='课程名')),
                ('xkh', models.CharField(max_length=50, verbose_name='选课号')),
                ('xkb', models.CharField(max_length=10, verbose_name='选课币')),
                ('year', models.CharField(max_length=10, verbose_name='学年')),
                ('xf', models.FloatField(verbose_name='学分')),
                ('teacher', models.CharField(max_length=100, verbose_name='任课老师')),
            ],
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='username')),
                ('password', models.CharField(max_length=120, verbose_name='password')),
                ('mail', models.EmailField(max_length=120, verbose_name='email')),
                ('openid', models.CharField(max_length=120, verbose_name='openid')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.WeixinInfo')),
            ],
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coursename', models.CharField(max_length=200, verbose_name='课程名')),
                ('coursetype', models.CharField(max_length=50, verbose_name='课程类型')),
                ('year', models.CharField(max_length=10, verbose_name='学年')),
                ('score', models.CharField(max_length=40, verbose_name='成绩')),
                ('jd', models.FloatField(verbose_name='绩点')),
                ('xf', models.FloatField(verbose_name='学分')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AddonOucJw.StudentInfo')),
            ],
        ),
        migrations.AddField(
            model_name='studentcourse',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AddonOucJw.StudentInfo'),
        ),
    ]