# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170809_1638'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmployeeManager',
            new_name='EmployeeSupervisor',
        ),
        migrations.RenameField(
            model_name='employeesupervisor',
            old_name='manager',
            new_name='supervisor',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='managers',
        ),
        migrations.AddField(
            model_name='employee',
            name='supervisors',
            field=models.ManyToManyField(through='api.EmployeeSupervisor', to='api.Employee'),
        ),
    ]
