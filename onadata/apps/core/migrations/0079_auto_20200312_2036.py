# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_auto_20200204_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiary',
            name='nra_card_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='activityaggregatehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 12, 20, 36, 3, 272227)),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 12, 20, 36, 3, 270787), blank=True),
        ),
    ]
