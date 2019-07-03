# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0064_auto_20190703_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beneficiary',
            old_name='ward_no',
            new_name='ward_number',
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 3, 13, 43, 9, 617099), blank=True),
        ),
    ]
