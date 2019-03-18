# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20190317_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clusteractivity',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='clusteractivitygroup',
            name='activity_group',
        ),
        migrations.RemoveField(
            model_name='activitygroup',
            name='cluster',
        ),
        migrations.AlterField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(related_name='user_roles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ClusterActivity',
        ),
        migrations.DeleteModel(
            name='ClusterActivityGroup',
        ),
    ]
