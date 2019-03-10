# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_cluster'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=400)),
                ('type_id', models.IntegerField()),
                ('cluster', models.ForeignKey(related_name='beneficiary', to='core.Cluster')),
            ],
        ),
    ]
