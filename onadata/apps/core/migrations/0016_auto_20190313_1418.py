# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_userrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='form',
            field=models.ForeignKey(related_name='actform', blank=True, to='logger.XForm', null=True),
        ),
    ]
