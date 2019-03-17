# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20190317_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='AG_Id',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='published',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='target_complete',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='target_met',
        ),
    ]
