# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_output_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='output',
            name='project',
            field=models.ForeignKey(related_name='output', default=0, to='core.Project'),
            preserve_default=False,
        ),
    ]
