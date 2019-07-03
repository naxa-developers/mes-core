# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_auto_20190703_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beneficiary',
            old_name='ward_number',
            new_name='ward_no',
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 3, 13, 43, 40, 295130), blank=True),
        ),
    ]
