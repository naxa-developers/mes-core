# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_project_cluster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='beneficiaries',
            field=models.BooleanField(),
        ),
    ]
