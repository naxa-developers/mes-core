# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_auto_20190703_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiary',
            name='Remarks',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 3, 13, 40, 3, 716839), blank=True),
        ),
    ]
