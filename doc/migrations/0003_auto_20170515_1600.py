# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0002_auto_20170515_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymdoc',
            name='datestr',
            field=models.CharField(default=b'', max_length=64),
        ),
        migrations.AlterField(
            model_name='gymdoc',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 15, 16, 0, 30, 704836)),
        ),
        migrations.AlterField(
            model_name='gymvideo',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 15, 16, 0, 30, 705487)),
        ),
    ]
