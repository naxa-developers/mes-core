# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_auto_20190514_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beneficiary',
            old_name='GovernmentTranch',
            new_name='Tranch',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='Remarks',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='ward_no',
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='ward',
            field=models.IntegerField(null=True, verbose_name=b'ward', blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 20, 15, 55, 32, 139426), blank=True),
        ),
    ]
