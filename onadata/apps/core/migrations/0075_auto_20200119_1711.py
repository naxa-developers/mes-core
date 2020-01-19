# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_auto_20200118_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityaggregatehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 19, 17, 11, 33, 452789), blank=True),
        ),
    ]
