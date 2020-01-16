# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_auto_20191231_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityaggregate',
            name='activity',
        ),
        migrations.AddField(
            model_name='activityaggregate',
            name='name',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 16, 10, 55, 0, 734221), blank=True),
        ),
    ]
