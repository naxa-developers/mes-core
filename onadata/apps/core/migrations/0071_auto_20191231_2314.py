# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0070_auto_20191218_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityAggregate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aggregation_fields', jsonfield.fields.JSONField(default=list)),
                ('aggregation_fields_value', jsonfield.fields.JSONField(default={})),
                ('activity', models.ForeignKey(related_name='aggregations', to='core.Activity')),
            ],
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 31, 23, 14, 16, 50218), blank=True),
        ),
    ]
