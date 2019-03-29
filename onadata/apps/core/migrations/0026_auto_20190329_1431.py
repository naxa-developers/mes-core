# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20190329_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='target_number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='target_unit',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
