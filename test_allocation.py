#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.project.serializers import ProjectSerializer
from apps.employee.models import Employee

# Test data that mimics a real API request
test_data = {
    "project_id": "TEST-001",
    "project_name": "Test Project",
    "description": "Test Description",
    "project_manager": "Test Manager",
    "department": "IT",
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "status": "planning",
    "allocations": [
        {
            "employee_id": 1,
            "allocation": 50.0
        }
    ]
}

print("=== TESTING PROJECT CREATION WITH ALLOCATIONS ===")
print(f"Test data: {test_data}")

# Check if employee exists
try:
    employee = Employee.objects.get(id=1)
    print(f"Employee found: {employee}")
except Employee.DoesNotExist:
    print("Employee with ID 1 does not exist!")
    sys.exit(1)
except Exception as e:
    print(f"Error finding employee: {e}")
    sys.exit(1)

# Test serializer validation
serializer = ProjectSerializer(data=test_data)
print(f"Serializer is valid: {serializer.is_valid()}")

if not serializer.is_valid():
    print(f"Validation errors: {serializer.errors}")
else:
    print("Creating project...")
    try:
        project = serializer.save()
        print(f"Project created: {project}")
        print(f"Allocations created: {project.allocations.count()}")
        
        # Check allocations
        for allocation in project.allocations.all():
            print(f"  - {allocation.employee}: {allocation.allocation}%")
            
    except Exception as e:
        print(f"Error creating project: {e}")
        import traceback
        traceback.print_exc()
