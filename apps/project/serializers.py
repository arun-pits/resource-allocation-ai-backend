from rest_framework import serializers
from .models import Project, ProjectAllocation
from apps.employee.models import Employee
from apps.employee.serializers import EmployeeSerializer
from django.contrib.auth import authenticate, get_user_model


# ---------------------------------------------------
# Allocation (Basic)
# ---------------------------------------------------
class ProjectAllocationSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)
    employee_data = EmployeeSerializer(source='employee', read_only=True)

    class Meta:
        model = ProjectAllocation
        fields = ['id', 'employee_id', 'employee_data', 'allocation', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'employee_data']


# ---------------------------------------------------
# Allocation (Detail Version for Project Detail View)
# ---------------------------------------------------
class ProjectAllocationDetailSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = ProjectAllocation
        fields = ['id', 'employee', 'allocation', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# ---------------------------------------------------
# Project (Basic for list/create/update)
# ---------------------------------------------------
class ProjectSerializer(serializers.ModelSerializer):
    allocations = ProjectAllocationSerializer(many=True, required=False)
    team_members = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'project_id', 'project_name', 'description', 'project_manager',
            'department', 'url', 'devops_url', 'start_date', 'end_date', 'status',
            'allocations', 'team_members', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'team_members']

    def create(self, validated_data):
        allocations_data = validated_data.pop('allocations', [])
        project = Project.objects.create(**validated_data)

        for allocation_data in allocations_data:
            employee_id = allocation_data.get('employee_id')
            allocation_percent = allocation_data.get('allocation')

            try:
                employee = Employee.objects.get(id=employee_id)
                ProjectAllocation.objects.create(
                    project=project,
                    employee=employee,
                    allocation=allocation_percent
                )
            except Employee.DoesNotExist:
                continue

        return project

    def update(self, instance, validated_data):
        allocations_data = validated_data.pop('allocations', None)

        # Standard field updates
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Allocation updates
        if allocations_data is not None:
            instance.allocations.all().delete()

            for allocation_data in allocations_data:
                employee_id = allocation_data.get('employee_id')
                allocation_percent = allocation_data.get('allocation')

                try:
                    employee = Employee.objects.get(id=employee_id)
                    ProjectAllocation.objects.create(
                        project=instance,
                        employee=employee,
                        allocation=allocation_percent
                    )
                except Employee.DoesNotExist:
                    continue

        return instance

    def get_team_members(self, obj):
        allocations = obj.allocations.all()
        return ProjectAllocationSerializer(allocations, many=True).data


# ---------------------------------------------------
# Project (Detail Version for retrieve action)
# ---------------------------------------------------
class ProjectDetailSerializer(serializers.ModelSerializer):
    allocations = ProjectAllocationDetailSerializer(many=True, read_only=True)
    team_members = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'project_id', 'project_name', 'description', 'project_manager',
            'department', 'url', 'devops_url', 'start_date', 'end_date', 'status',
            'allocations', 'team_members', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_team_members(self, obj):
        return ProjectAllocationSerializer(obj.allocations.all(), many=True).data
