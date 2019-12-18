# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_auto_20191216_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 18, 13, 43, 40, 582218), blank=True),
        ),
        migrations.AlterOrderWithRespectTo(
            name='clustera',
            order_with_respect_to='activity',
        ),
    ]
