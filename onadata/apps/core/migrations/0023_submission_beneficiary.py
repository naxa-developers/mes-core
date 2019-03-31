# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='beneficiary',
            field=models.ForeignKey(related_name='submissions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.Beneficiary', null=True),
        ),
    ]
