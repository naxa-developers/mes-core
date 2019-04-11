# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20190405_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTimeInterval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('project', models.ForeignKey(related_name='interval', to='core.Project')),
            ],
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 5, 12, 55, 18, 814624), blank=True),
        ),
    ]
