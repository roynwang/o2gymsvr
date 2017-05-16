# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0003_auto_20170515_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymdoc',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 14, 8, 57, 826828)),
        ),
        migrations.AlterField(
            model_name='gymvideo',
            name='summary',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='gymvideo',
            name='title',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='gymvideo',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 14, 8, 57, 827759)),
        ),
    ]
