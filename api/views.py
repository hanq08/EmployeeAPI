# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
from .serializers import EmployeeSerializer, RoleSerializer, SupervisorSerializer, EmployeePatchSerializer, \
    EmployeePromotionSerializer, EmployeeUpdateSerializer, RoleDetailSerializer, HierarchySerializer
from .models import Employee, Role, EmployeeSupervisor

class HierarchyView(generics.ListAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Employee.objects.all()
    serializer_class = HierarchySerializer

class CreateEmployeeView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new employee."""
        serializer.save()

class DetailsEmployeeView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Employee.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return EmployeePatchSerializer
        return EmployeeUpdateSerializer

class CreateRoleView(generics.ListAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    def perform_create(self, serializer):
        """Save the post data when creating a new role."""
        serializer.save()

class DetailsRoleView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Role.objects.all()
    serializer_class = RoleDetailSerializer

class CreateSupervisorsView(generics.ListCreateAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = EmployeeSupervisor.objects.all()
    serializer_class = SupervisorSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new employee."""
        serializer.save()

class DetailsSupervisorsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = EmployeeSupervisor.objects.all()
    serializer_class = SupervisorSerializer


class PromoteEmployeeView(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeePromotionSerializer