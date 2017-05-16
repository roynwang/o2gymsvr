# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0004_auto_20170516_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymvideo',
            name='datestr',
            field=models.CharField(default=b'', max_length=64),
        ),
        migrations.AlterField(
            model_name='gymdoc',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 14, 56, 24, 416176)),
        ),
        migrations.AlterField(
            model_name='gymvideo',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 14, 56, 24, 417014)),
        ),
    ]
