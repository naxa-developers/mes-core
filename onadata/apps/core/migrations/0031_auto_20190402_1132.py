# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20190402_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='weight',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 2, 11, 32, 10, 46438), blank=True),
        ),
    ]
