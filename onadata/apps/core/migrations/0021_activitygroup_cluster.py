# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20190318_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitygroup',
            name='cluster',
            field=models.ForeignKey(related_name='activity_group', default=1, to='core.Cluster'),
            preserve_default=False,
        ),
    ]
