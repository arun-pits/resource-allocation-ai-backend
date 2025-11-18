#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.project.models import Project, ProjectAllocation
from apps.employee.models import Employee

print("=== DATABASE RECORDS CHECK ===")
print(f"Projects count: {Project.objects.count()}")
print(f"ProjectAllocations count: {ProjectAllocation.objects.count()}")
print(f"Employees count: {Employee.objects.count()}")

print("\n=== PROJECT DETAILS ===")
for project in Project.objects.all()[:3]:
    print(f"Project: {project.project_name} (ID: {project.id})")
    allocations = project.allocations.all()
    print(f"  Allocations: {allocations.count()}")
    for allocation in allocations:
        print(f"    - {allocation.employee.first_name} {allocation.employee.last_name}: {allocation.allocation}%")
    print()

print("\n=== EMPLOYEE DETAILS ===")
for employee in Employee.objects.all()[:3]:
    print(f"Employee: {employee.first_name} {employee.last_name} (ID: {employee.id})")
    allocations = employee.project_allocations.all()
    print(f"  Project Allocations: {allocations.count()}")
    for allocation in allocations:
        print(f"    - {allocation.project.project_name}: {allocation.allocation}%")
    print()
