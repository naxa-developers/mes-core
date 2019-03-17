# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20190313_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClusterActivityGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_group', models.ForeignKey(related_name='clusteractivitygroup', to='core.ActivityGroup')),
            ],
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='identifier',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='type_id',
        ),
        migrations.AlterField(
            model_name='activity',
            name='AG_Id',
            field=models.IntegerField(null=True, verbose_name=b'Activity Group ID', blank=True),
        ),
        migrations.AddField(
            model_name='clusteractivity',
            name='activity',
            field=models.ForeignKey(related_name='clusteractivity', to='core.Activity'),
        ),
    ]
