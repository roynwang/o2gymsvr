# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64, db_index=True)),
                ('feedback', models.CharField(default=b'', max_length=1024)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 11, 17, 9, 34, 11, 595164))),
            ],
        ),
    ]
