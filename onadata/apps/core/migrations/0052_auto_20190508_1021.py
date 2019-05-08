# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_auto_20190424_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='latitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=12),
        ),
        migrations.AddField(
            model_name='activity',
            name='longitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=12),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='latitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=12),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='longitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=12),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 8, 10, 21, 26, 759443), blank=True),
        )
    ]
