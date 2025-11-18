#!/usr/bin/env python
import os
import sys
import django

print("Starting Django setup...")
try:
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()
    print("Django setup completed")

    from apps.project.serializers import ProjectSerializer
    from apps.employee.models import Employee
    print("Imports successful")
except Exception as e:
    print(f"Error during setup: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test data that mimics the CORRECTED frontend request
test_data = {
    "project_id": "TEST-002",
    "project_name": "Test Project with Fixed Payload",
    "description": "Testing with correct allocations field name",
    "project_manager": "Test Manager",
    "department": "IT",
    "start_date": "2025-01-15",
    "end_date": "2025-12-31",
    "status": "planning",
    "allocations": [
        {
            "employee_id": 1,
            "allocation": 75.0
        }
    ]
}

print("=== TESTING FIXED PAYLOAD FORMAT ===")
print(f"Test data: {test_data}")

# Test serializer validation and creation
serializer = ProjectSerializer(data=test_data)
print(f"Serializer is valid: {serializer.is_valid()}")

if not serializer.is_valid():
    print(f"Validation errors: {serializer.errors}")
else:
    print("Creating project with fixed payload...")
    try:
        project = serializer.save()
        print(f"✓ Project created: {project}")
        print(f"✓ Allocations created: {project.allocations.count()}")
        
        # Check allocations details
        for allocation in project.allocations.all():
            print(f"  - {allocation.employee}: {allocation.allocation}%")
            
        print("\n=== SUCCESS: Project allocations created properly! ===")
            
    except Exception as e:
        print(f"✗ Error creating project: {e}")
        import traceback
        traceback.print_exc()
