# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0005_auto_20170516_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymvideo',
            name='pic',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gymdoc',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 6, 13, 30, 45, 815926)),
        ),
        migrations.AlterField(
            model_name='gymvideo',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 6, 13, 30, 45, 816769)),
        ),
    ]
