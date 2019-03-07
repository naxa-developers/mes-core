# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190307_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('AG_Id', models.IntegerField(verbose_name=b'Activity Group ID')),
                ('target_number', models.IntegerField()),
                ('target_unit', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('form_id', models.IntegerField()),
                ('target_complete', models.BooleanField(default=True)),
                ('beneficiary_level', models.BooleanField(default=True)),
                ('published', models.BooleanField(default=True)),
                ('target_met', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('output', models.ForeignKey(related_name='activity_group', to='core.Output')),
                ('project', models.ForeignKey(related_name='activity_group', to='core.Project')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_group',
            field=models.ForeignKey(related_name='activity', to='core.ActivityGroup'),
        ),
    ]
