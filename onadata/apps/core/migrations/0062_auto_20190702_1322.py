# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_auto_20190628_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beneficiary',
            old_name='Type',
            new_name='vulnerabilityType',
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='category',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='address',
            field=models.CharField(max_length=400, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 2, 13, 22, 29, 191861), blank=True),
        ),
    ]
