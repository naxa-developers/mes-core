# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0076_auto_20200119_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='entry_form',
            field=models.ForeignKey(related_name='entry_forms', blank=True, to='core.Activity', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='is_entry',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activity',
            name='is_registration',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityaggregatehistory',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 1, 20, 32, 53, 437055)),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 1, 20, 32, 53, 429847), blank=True),
        ),
    ]
