# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoachSalarySetting',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('coach', models.IntegerField()),
                ('base_salary', models.FloatField(default=0)),
                ('yanglao', models.FloatField(default=0)),
                ('yiliao', models.FloatField(default=0)),
                ('shiye', models.FloatField(default=0)),
                ('gongjijin', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GymFee',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('gym', models.IntegerField(unique=True, db_index=True)),
                ('balance', models.IntegerField(unique=True, db_index=True)),
                ('coaches', models.TextField(default=b'[]')),
                ('coach_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='coachsalarysetting',
            name='gymfee',
            field=models.ForeignKey(related_name='coach_salary_setting', to='fee.GymFee'),
        ),
    ]
