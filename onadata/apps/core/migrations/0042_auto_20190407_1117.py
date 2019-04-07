# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20190405_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterAHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target_number', models.IntegerField(default=0, null=True, blank=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='clustera',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='clustera',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='clustera',
            name='target_update_at',
        ),
        migrations.AddField(
            model_name='clustera',
            name='time_interval',
            field=models.ForeignKey(related_name='cainterval', blank=True, to='core.ProjectTimeInterval', null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 7, 11, 17, 48, 635073), blank=True),
        ),
        migrations.AddField(
            model_name='clusterahistory',
            name='clustera',
            field=models.ForeignKey(related_name='history', to='core.ClusterA'),
        ),
        migrations.AddField(
            model_name='clusterahistory',
            name='time_interval',
            field=models.ForeignKey(related_name='cahistory', blank=True, to='core.ProjectTimeInterval', null=True),
        ),
    ]
