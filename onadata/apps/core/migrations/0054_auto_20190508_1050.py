# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20190508_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustera',
            name='latitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=15),
        ),
        migrations.AddField(
            model_name='clustera',
            name='longitude',
            field=models.DecimalField(default=0.0, max_digits=19, decimal_places=15),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 8, 10, 50, 6, 80321), blank=True),
        )
    ]
