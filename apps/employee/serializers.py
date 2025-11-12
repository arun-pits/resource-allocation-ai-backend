from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'first_name',
            'last_name',
            'employee_email',
            'employee_ph_no',
            'designation',
            'employee_id',
            'department',
            'manager',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_employee_id(self, value):
        """Validate that employee ID is unique during creation"""
        # During update, the instance is available, so we exclude current instance
        if self.instance:
            if Employee.objects.filter(employee_id=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Employee ID already exists.")
        else:
            # During creation
            if Employee.objects.filter(employee_id=value).exists():
                raise serializers.ValidationError("Employee ID already exists.")
        return value

    def validate_employee_email(self, value):
        """Validate that email is unique during creation"""
        # During update, the instance is available, so we exclude current instance
        if self.instance:
            if Employee.objects.filter(employee_email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Employee email already exists.")
        else:
            # During creation
            if Employee.objects.filter(employee_email=value).exists():
                raise serializers.ValidationError("Employee email already exists.")
        return value

    def validate(self, data):
        """
        Object-level validation
        """
        # Add any cross-field validation here if needed
        return data