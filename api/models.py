# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rank = models.IntegerField(default=1)

class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    salary = models.IntegerField(default=80000)
    performance_review = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=3)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    supervisors = models.ManyToManyField('self', through="EmployeeSupervisor", symmetrical=False)

class EmployeeSupervisor(models.Model):
    employee = models.ForeignKey(Employee, related_name='source')
    supervisor = models.ForeignKey(Employee, related_name='target')
