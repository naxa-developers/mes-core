# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20190403_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustera',
            name='target_number',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='clustera',
            name='target_unit',
            field=models.CharField(default=b'', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 3, 14, 49, 8, 315516), blank=True),
        ),
    ]
