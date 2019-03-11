# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0011_add-index-to-instance-uuid_and_xform_uuid'),
        ('core', '0007_beneficiary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='form_id',
        ),
        migrations.AddField(
            model_name='activity',
            name='form',
            field=models.ForeignKey(related_name='actform', default=0, to='logger.XForm'),
            preserve_default=False,
        ),
    ]
