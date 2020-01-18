# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0073_auto_20200116_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityaggregate',
            name='project',
            field=models.ForeignKey(related_name='aggregations', blank=True, to='core.Project', null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 18, 17, 21, 30, 544864), blank=True),
        ),
    ]
