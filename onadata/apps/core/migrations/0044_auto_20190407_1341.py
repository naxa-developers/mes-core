# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20190407_1305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clusterahistory',
            old_name='target_number',
            new_name='target_completed',
        ),
        migrations.AddField(
            model_name='clustera',
            name='target_completed',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 7, 13, 40, 58, 684635), blank=True),
        ),
    ]
