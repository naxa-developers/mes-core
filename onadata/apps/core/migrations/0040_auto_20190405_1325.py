# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20190405_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='range',
        ),
        migrations.AddField(
            model_name='activity',
            name='time_interval',
            field=models.ForeignKey(related_name='activity_interval', blank=True, to='core.ProjectTimeInterval', null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 5, 13, 25, 39, 197751), blank=True),
        ),
    ]
