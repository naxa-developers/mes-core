# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20190326_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
