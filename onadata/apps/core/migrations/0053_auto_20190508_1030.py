# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_auto_20190508_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='latitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=15),
        ),
        migrations.AlterField(
            model_name='activity',
            name='longitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=15),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='latitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=15),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='longitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=15),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 8, 10, 30, 37, 694024), blank=True),
        )
    ]
