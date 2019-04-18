# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20190410_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('district', models.ForeignKey(related_name='municipality', to='core.District')),
            ],
        ),
        migrations.RemoveField(
            model_name='cluster',
            name='district',
        ),
        migrations.RemoveField(
            model_name='cluster',
            name='municipality',
        ),
        migrations.AlterField(
            model_name='config',
            name='activity_group_updated',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 15, 13, 14, 37, 951513), blank=True),
        ),
        migrations.AddField(
            model_name='cluster',
            name='municipality',
            field=models.ManyToManyField(related_name='cluster', to='core.Municipality'),
        ),
    ]
