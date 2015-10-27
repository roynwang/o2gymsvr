# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutAction',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('workouttype', models.CharField(max_length=32)),
                ('by', models.CharField(default=b'', max_length=64, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutCategeory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('icon', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='workoutaction',
            name='categeory',
            field=models.ForeignKey(related_name='actions', to='traincategory.WorkoutCategeory'),
        ),
    ]
