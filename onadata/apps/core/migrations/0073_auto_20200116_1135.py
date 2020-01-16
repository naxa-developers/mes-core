# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0072_auto_20200116_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityAggregateHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aggregation_values', jsonfield.fields.JSONField(default={})),
            ],
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 16, 11, 35, 48, 421758), blank=True),
        ),
    ]
