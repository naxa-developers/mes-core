# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_auto_20190801_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='order',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 16, 14, 44, 56, 62558), blank=True),
        ),
    ]
