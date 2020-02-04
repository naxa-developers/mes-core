# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_auto_20200201_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='beneficiary_group',
            field=models.ForeignKey(related_name='beneficiary_activity', blank=True, to='core.ActivityGroup', null=True),
        ),
        migrations.AlterField(
            model_name='activityaggregatehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 4, 10, 2, 50, 21923)),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 4, 10, 2, 50, 20730), blank=True),
        ),
    ]
