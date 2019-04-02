# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beneficiary',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='activitygroup',
            name='weight',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 2, 10, 40, 46, 762678), blank=True),
        ),
    ]
