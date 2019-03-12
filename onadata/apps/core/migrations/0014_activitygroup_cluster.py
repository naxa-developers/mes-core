# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_cluster_activity_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitygroup',
            name='cluster',
            field=models.ForeignKey(related_name='activitygroup', default=0, to='core.Cluster'),
            preserve_default=False,
        ),
    ]
