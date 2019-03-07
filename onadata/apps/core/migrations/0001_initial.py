# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('sector', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('reporting_period', models.IntegerField(choices=[(1, b'Monthly'), (2, b'Bi-annually'), (3, b'Quaterly')])),
                ('cluster', models.BooleanField(default=True)),
                ('beneficiaries', models.BooleanField(default=True)),
            ],
        ),
    ]
