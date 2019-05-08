# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20190508_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 8, 11, 30, 5, 508562), blank=True),
        ),
        migrations.RemoveField(
            model_name='userrole',
            name='cluster',
        ),
        migrations.AddField(
            model_name='userrole',
            name='cluster',
            field=models.ManyToManyField(related_name='userrole_cluster', null=True, to='core.Cluster', blank=True),
        ),
    ]
