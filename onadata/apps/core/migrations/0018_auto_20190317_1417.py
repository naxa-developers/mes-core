# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20190317_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiary',
            name='Type',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='ward_no',
            field=models.IntegerField(default=0, verbose_name=b'ward number'),
            preserve_default=False,
        ),
    ]
