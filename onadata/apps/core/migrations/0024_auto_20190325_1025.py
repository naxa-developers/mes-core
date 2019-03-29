# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_submission_beneficiary'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiary',
            name='ConstructionPhase',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='GovernmentTranch',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='Remarks',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='Typesofhouse',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
