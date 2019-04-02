# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20190329_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='cluster',
            field=models.ForeignKey(related_name='userrole_cluster', blank=True, to='core.Cluster', null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='group',
            field=models.ForeignKey(related_name='userrole_group', to='auth.Group'),
        ),
    ]
