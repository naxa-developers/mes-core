# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_auto_20200119_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityaggregatehistory',
            name='aggregation',
            field=models.ForeignKey(related_name='history', blank=True, to='core.ActivityAggregate', null=True),
        ),
        migrations.AlterField(
            model_name='activityaggregatehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 19, 17, 23, 58, 981492)),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 19, 17, 23, 58, 979589), blank=True),
        ),
    ]
