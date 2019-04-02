# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20190325_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustera',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='clustera',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
