# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from models import Employee, Role, EmployeeSupervisor
from django.core.management import call_command
from django.test import Client
from rest_framework import serializers

class ModelTestCase(TestCase):
    """This calss defines the test suite for the employee model"""
    c = Client()
    def setUp(self):
        """Define the test client and other test variables."""
        call_command("loaddata", "role.json")

    def test_employee_read(self):
        """Test the employee model can create a employee."""
        response = self.c.get('/employee', follow=True)
        self.assertEqual(200, response.status_code)

    def test_employee_create(self):
        """Test the employee model can create a employee."""
        response = self.c.post('/employee', {'first_name': 'Fake', 'last_name': 'Doe', 'role_id':1, 'supervisor_id':1}, follow=True)
        self.assertEqual(200, response.status_code)

    def test_employee_supervisor_create(self):
        response = self.c.post('/supervisors',
                               {'employees':2, 'supervisors':1},
                               follow=True)
        self.assertEqual(200, response.status_code)

    def test_validate_rank(self):
        response = self.c.post('/supervisors/',
                               {'employees': 1, 'supervisors': 2},
                               follow=True)
        self.assertEqual(400, response.status_code)
