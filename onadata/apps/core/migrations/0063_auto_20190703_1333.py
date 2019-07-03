# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_auto_20190702_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beneficiary',
            old_name='Tranch',
            new_name='GovernmentTranch',
        ),
        migrations.RenameField(
            model_name='beneficiary',
            old_name='category',
            new_name='Type',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='ward',
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='ward_no',
            field=models.IntegerField(null=True, verbose_name=b'ward number', blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 3, 13, 33, 35, 163657), blank=True),
        ),
    ]
