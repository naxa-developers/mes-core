# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20190402_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.CharField(default=b'pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 3, 13, 8, 37, 731018), blank=True),
        ),
    ]
