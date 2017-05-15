# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GymDoc',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('gym', models.IntegerField()),
                ('author', models.CharField(max_length=128)),
                ('title', models.IntegerField(max_length=256)),
                ('summary', models.IntegerField(max_length=256)),
                ('attachment', models.CharField(max_length=256)),
                ('update', models.DateTimeField(default=datetime.datetime(2017, 5, 15, 13, 14, 35, 989523))),
            ],
        ),
        migrations.CreateModel(
            name='GymVideo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('gym', models.IntegerField()),
                ('uploader', models.CharField(max_length=128)),
                ('coach', models.CharField(max_length=128)),
                ('title', models.IntegerField(max_length=256)),
                ('summary', models.IntegerField(max_length=1024)),
                ('attachment', models.CharField(max_length=256)),
                ('update', models.DateTimeField(default=datetime.datetime(2017, 5, 15, 13, 14, 35, 990457))),
            ],
        ),
        migrations.CreateModel(
            name='GymVideoKeyword',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('gym', models.IntegerField()),
                ('keyword', models.CharField(max_length=128)),
                ('videoid', models.IntegerField()),
            ],
        ),
    ]
