# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0011_add-index-to-instance-uuid_and_xform_uuid'),
        ('core', '0021_auto_20190319_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cluster_activity', models.ForeignKey(related_name='submissions', to='core.ClusterA')),
                ('instance', models.OneToOneField(related_name='submission', to='logger.Instance')),
            ],
        ),
    ]
