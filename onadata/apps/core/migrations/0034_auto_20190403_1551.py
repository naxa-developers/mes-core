# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20190403_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustera',
            name='target_update_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 3, 15, 51, 10, 367086), blank=True),
        ),
    ]
