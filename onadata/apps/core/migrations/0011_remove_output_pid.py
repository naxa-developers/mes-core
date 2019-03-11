# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_activity_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='output',
            name='PID',
        ),
    ]
