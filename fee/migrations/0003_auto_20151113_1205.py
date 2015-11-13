# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0002_auto_20151112_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachsalarysetting',
            name='xiaoshou',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='coachsalarysetting',
            name='xuke',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='gymfee',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]
