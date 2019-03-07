# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190307_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('PID', models.IntegerField(verbose_name=b'Project Id')),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='beneficiaries',
            field=models.BooleanField(default=True),
        ),
    ]
