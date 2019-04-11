# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20190407_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustera',
            name='interval_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 7, 14, 11, 46, 995453), blank=True),
        ),
    ]
