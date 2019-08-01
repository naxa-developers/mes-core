# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_auto_20190705_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='vulnerabilityType',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 1, 13, 28, 1, 589466), blank=True),
        ),
    ]
