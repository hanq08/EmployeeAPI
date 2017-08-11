from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from .models import Employee, Role, EmployeeSupervisor
from django.db import transaction
from django.db.models import Max


class RolePrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return '%s' % (instance.name)

class EmployeePrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return '%s %s - %s' % (instance.first_name, instance.last_name, instance.role.name)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id','name','rank')
        read_only_fields = ('rank','name')
        validators = [
            UniqueValidator(queryset=Role.objects.all())
        ]

class RoleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id','name','rank')
        read_only_fields = ('rank',)
        validators = [
            UniqueValidator(queryset=Role.objects.all())
        ]

class SupervisorSerializer(serializers.ModelSerializer):
    employees = EmployeePrimaryKeyRelatedField(queryset=Employee.objects.all(), source='employee', write_only=True)
    supervisors = EmployeePrimaryKeyRelatedField(queryset=Employee.objects.all(), source='supervisor',write_only=True)
    class Meta:
        model = EmployeeSupervisor
        fields = ('id','employees','supervisors', 'employee', 'supervisor')
        read_only_fields = ('employee', 'supervisor')
        validators = [
            UniqueTogetherValidator(
                queryset=EmployeeSupervisor.objects.all(),
                fields=('employee', 'supervisor')
            )
        ]
    def validate(self, data):
        employee = data['employee']
        supervisor = data['supervisor']
        if employee.role != Role.objects.get(name="Individual Contributor") and EmployeeSupervisor.objects.filter(employee=employee).count() == 3:
            raise serializers.ValidationError("Employee can't have more than three direct reports")
        employee_rank = employee.role.rank
        supervisor_rank = supervisor.role.rank
        if employee_rank > supervisor_rank:
            raise serializers.ValidationError("supervisor rank should be higher or equal to employee")
        return data

class HierarchySerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    role = RoleSerializer(read_only=True)
    supervisors = EmployeePrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'role', 'supervisors')

class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    role = RoleSerializer(read_only=True)
    role_id = RolePrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)
    supervisors = EmployeePrimaryKeyRelatedField(many=True,read_only=True)
    supervisor_id = EmployeePrimaryKeyRelatedField(queryset=Employee.objects.all(), write_only=True)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'salary', 'phone', 'role', 'role_id', 'supervisor_id', 'performance_review','supervisors')
        validators = [
            UniqueTogetherValidator(
                queryset=Employee.objects.all(),
                fields=('first_name', 'last_name')
            ),
        ]
    def validate(self, data):
        supervisor = data['supervisor_id']
        employee_rank = data['role'].rank
        supervisor_rank = supervisor.role.rank
        if employee_rank > supervisor_rank:
            raise serializers.ValidationError("supervisor rank should be higher or equal to employee")
        return data
    def create(self, validated_data):
        supervisor = validated_data.pop('supervisor_id')
        employee = Employee.objects.create(**validated_data)

        EmployeeSupervisor.objects.create(employee=employee,supervisor=supervisor)
        return employee

class EmployeeUpdateSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    role = RoleSerializer(read_only=True)
    #roles = RolePrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)
    supervisors = EmployeePrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'salary', 'phone', 'role', 'performance_review','supervisors')
        validators = [
            UniqueTogetherValidator(
                queryset=Employee.objects.all(),
                fields=('first_name', 'last_name')
            ),
        ]

class EmployeePatchSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'salary', 'phone')
        read_only_fields=('roles','supervisor_id')
        validators = [
            UniqueTogetherValidator(
                queryset=Employee.objects.all(),
                fields=('first_name', 'last_name')
            )
        ]
    def validate(self, data):
        return data

class EmployeePromotionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    supervisors = EmployeePrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = ('id', 'role', 'supervisors')
    def update(self, instance, validated_data):
        new_rank = min(Role.objects.all().aggregate(Max('rank'))['rank__max'], instance.role.rank+1)
        new_role = Role.objects.get(rank=new_rank)
        instance.role = new_role
        new_supervisor = instance.supervisors.first().supervisors.first()
        with transaction.atomic():
            EmployeeSupervisor.objects.filter(employee=instance).delete()
            EmployeeSupervisor.objects.create(employee=instance, supervisor=new_supervisor)
            instance.save()
        return instance