# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190307_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('district', models.CharField(max_length=200)),
                ('municipality', models.CharField(max_length=200)),
                ('ward', models.CharField(max_length=200)),
                ('activity_group', models.ForeignKey(related_name='cluster', to='core.ActivityGroup')),
                ('project', models.ForeignKey(related_name='cluster', to='core.Project')),
            ],
        ),
    ]
