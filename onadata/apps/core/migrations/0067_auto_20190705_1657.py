# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_auto_20190703_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='cluster',
            field=models.ForeignKey(related_name='beneficiary', blank=True, to='core.Cluster', null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 5, 16, 57, 31, 3836), blank=True),
        ),
    ]
