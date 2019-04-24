# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='clustera_history',
            field=models.ForeignKey(related_name='submissions', blank=True, to='core.ClusterAHistory', null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 24, 10, 58, 40, 851059), blank=True),
        ),
    ]
