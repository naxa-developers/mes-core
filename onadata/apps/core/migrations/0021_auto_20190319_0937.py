# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20190318_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity', models.ForeignKey(related_name='clustera', to='core.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='ClusterAG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_group', models.ForeignKey(related_name='clusterag', to='core.ActivityGroup')),
                ('cluster', models.ForeignKey(related_name='clusterag', to='core.Cluster')),
            ],
        ),
        migrations.AddField(
            model_name='clustera',
            name='cag',
            field=models.ForeignKey(related_name='ca', to='core.ClusterAG'),
        ),
    ]
