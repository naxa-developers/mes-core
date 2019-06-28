# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_auto_20190530_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiary',
            name='payment_type',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'single', b'One Time Payment'), (b'daily', b'Daily Basis')]),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 28, 14, 48, 40, 368776), blank=True),
        ),
    ]
