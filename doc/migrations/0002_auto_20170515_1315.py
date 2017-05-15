# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymdoc',
            name='summary',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='gymdoc',
            name='title',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='gymdoc',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 15, 13, 15, 21, 212600)),
        ),
        migrations.AlterField(
            model_name='gymvideo',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 15, 13, 15, 21, 213796)),
        ),
    ]
