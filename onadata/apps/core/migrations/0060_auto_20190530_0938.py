# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_auto_20190520_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 30, 9, 38, 1, 846691), blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='reporting_period',
            field=models.IntegerField(choices=[(1, b'Monthly'), (2, b'Bi-annually'), (3, b'Quarterly')]),
        ),
    ]
