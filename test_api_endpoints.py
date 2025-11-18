#!/usr/bin/env python3
"""
API Test Script for ViewProject Django Backend
Tests the actual HTTP endpoints to ensure they work correctly.
"""
import requests
import json
from datetime import date, timedelta

# Base URL for the Django server
BASE_URL = "http://localhost:8000/api"

def test_api_endpoints():
    """Test all ViewProject related API endpoints"""
    
    print("🚀 Testing ViewProject Django Backend API")
    print("=" * 50)
    
    # Test 1: Get all projects (to find a test project)
    print("\n1️⃣  Testing GET /api/projects/")
    try:
        response = requests.get(f"{BASE_URL}/projects/")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data.get('count', 0)} projects")
            
            if data.get('projects') and len(data['projects']) > 0:
                project_id = data['projects'][0]['id']
                print(f"   📝 Using project ID: {project_id}")
                return project_id
            else:
                print("   ⚠️  No projects found. Creating test project needed.")
                return None
        else:
            print(f"   ❌ Failed to get projects: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_project_detail(project_id):
    """Test project detail endpoint"""
    
    print(f"\n2️⃣  Testing GET /api/projects/{project_id}/")
    try:
        response = requests.get(f"{BASE_URL}/projects/{project_id}/")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Project: {data.get('project_name', 'Unknown')}")
            print(f"   📊 Total Allocation: {data.get('total_allocated_percentage', 0)}%")
            print(f"   👥 Team Count: {data.get('team_count', 0)}")
            
            # Verify required fields are present
            required_fields = [
                'id', 'project_id', 'project_name', 'description', 
                'project_manager', 'department', 'start_date', 'end_date', 'status'
            ]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"   ⚠️  Missing required fields: {missing_fields}")
            else:
                print("   ✅ All required fields present")
            
            return True
        else:
            print(f"   ❌ Failed to get project detail: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_project_allocations(project_id):
    """Test project allocations endpoint"""
    
    print(f"\n3️⃣  Testing GET /api/projects/{project_id}/allocations/")
    try:
        response = requests.get(f"{BASE_URL}/projects/{project_id}/allocations/")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {len(data)} allocations")
            
            if data:
                allocation = data[0]
                print(f"   👤 First Employee: {allocation.get('employee', {}).get('first_name', 'Unknown')}")
                print(f"   💼 Allocation: {allocation.get('allocation', 0)}%")
                
                # Verify allocation structure
                required_fields = ['id', 'employee', 'allocation']
                missing_fields = [field for field in required_fields if field not in allocation]
                
                if missing_fields:
                    print(f"   ⚠️  Missing allocation fields: {missing_fields}")
                else:
                    print("   ✅ Allocation structure valid")
                    
                # Verify employee structure
                if 'employee' in allocation and allocation['employee']:
                    employee = allocation['employee']
                    emp_required_fields = ['id', 'first_name', 'last_name', 'employee_email']
                    emp_missing_fields = [field for field in emp_required_fields if field not in employee]
                    
                    if emp_missing_fields:
                        print(f"   ⚠️  Missing employee fields: {emp_missing_fields}")
                    else:
                        print("   ✅ Employee structure valid")
            else:
                print("   ℹ️  No allocations found for this project")
            
            return True
        else:
            print(f"   ❌ Failed to get project allocations: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_create_sample_project():
    """Create a sample project for testing"""
    
    print("\n🔨 Creating sample project for testing...")
    
    # Sample project data
    project_data = {
        "project_id": "TEST001",
        "project_name": "Test Project for ViewProject",
        "description": "This is a test project created for API testing.",
        "project_manager": "Test Manager",
        "department": "Engineering",
        "url": "https://github.com/company/test-project",
        "devops_url": "https://azure.devops.com/company/test-project",
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=90)).isoformat(),
        "status": "active",
        "allocations": []
    }
    
    try:
        response = requests.post(f"{BASE_URL}/projects/", 
                               json=project_data,
                               headers={'Content-Type': 'application/json'})
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            project_id = data.get('data', {}).get('id')
            print(f"   ✅ Created test project with ID: {project_id}")
            return project_id
        else:
            print(f"   ❌ Failed to create project: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    """Main test function"""
    
    # First, try to get existing projects
    project_id = test_api_endpoints()
    
    # If no projects exist, create a test project
    if project_id is None:
        project_id = test_create_sample_project()
    
    if project_id is None:
        print("\n❌ Unable to get or create a test project. Exiting.")
        return
    
    # Test project detail endpoint
    detail_success = test_project_detail(project_id)
    
    # Test project allocations endpoint
    allocations_success = test_project_allocations(project_id)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Project Detail API: {'✅ PASS' if detail_success else '❌ FAIL'}")
    print(f"Project Allocations API: {'✅ PASS' if allocations_success else '❌ FAIL'}")
    
    if detail_success and allocations_success:
        print("\n🎉 All tests passed! ViewProject.js backend is ready!")
    else:
        print("\n⚠️  Some tests failed. Check the Django backend implementation.")
    
    print(f"\n🔗 Test Project URL: http://localhost:3000/projects/{project_id}")
    print("   (Use this URL to test the ViewProject.js frontend)")

if __name__ == "__main__":
    print("Make sure Django server is running on http://localhost:8000")
    print("Run: python manage.py runserver 8000")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/projects/", timeout=5)
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Django server not running. Please start it first:")
        print("   cd backend")
        print("   python manage.py runserver 8000")
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
