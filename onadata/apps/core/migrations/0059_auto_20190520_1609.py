# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_auto_20190520_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiary',
            name='district',
            field=models.ForeignKey(blank=True, to='core.District', null=True),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='municipality',
            field=models.ForeignKey(blank=True, to='core.Municipality', null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 20, 16, 9, 1, 820067), blank=True),
        ),
    ]
