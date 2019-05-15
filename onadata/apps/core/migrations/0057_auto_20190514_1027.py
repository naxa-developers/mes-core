# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_auto_20190514_1015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='clustera',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='clustera',
            name='longitude',
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True),
        ),
        migrations.AddField(
            model_name='clustera',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, geography=True, blank=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 14, 10, 27, 16, 816892), blank=True),
        ),
    ]
