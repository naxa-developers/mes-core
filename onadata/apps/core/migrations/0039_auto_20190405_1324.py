# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20190405_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='start_date',
        ),
        migrations.AddField(
            model_name='activity',
            name='range',
            field=models.ForeignKey(related_name='activity_range', blank=True, to='core.ProjectTimeInterval', null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 5, 13, 24, 54, 965972), blank=True),
        ),
    ]
