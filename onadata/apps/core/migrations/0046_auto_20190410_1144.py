# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_auto_20190407_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustera',
            name='target_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clusterahistory',
            name='target_number',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 10, 11, 44, 9, 674342), blank=True),
        ),
    ]
