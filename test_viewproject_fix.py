"""
Quick test to verify the serializers work correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    """Test the project endpoints"""
    
    print("🧪 Testing ViewProject Django Endpoints")
    print("=" * 45)
    
    # Test 1: List all projects
    print("\n1. Testing GET /api/projects/")
    try:
        response = requests.get(f"{BASE_URL}/projects/", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: Found {data.get('count', 0)} projects")
            
            if data.get('projects'):
                project = data['projects'][0]
                project_id = project['id']
                print(f"📝 First project: {project.get('project_name', 'Unknown')} (ID: {project_id})")
                
                # Test 2: Get project detail
                print(f"\n2. Testing GET /api/projects/{project_id}/")
                detail_response = requests.get(f"{BASE_URL}/projects/{project_id}/", timeout=10)
                print(f"Status: {detail_response.status_code}")
                
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    print(f"✅ Project Detail Success")
                    print(f"   Name: {detail_data.get('project_name')}")
                    print(f"   Manager: {detail_data.get('project_manager')}")
                    print(f"   Status: {detail_data.get('status')}")
                    print(f"   Team Count: {detail_data.get('team_count', 0)}")
                    print(f"   Total Allocation: {detail_data.get('total_allocated_percentage', 0)}%")
                else:
                    print(f"❌ Project detail failed: {detail_response.text}")
                
                # Test 3: Get project allocations
                print(f"\n3. Testing GET /api/projects/{project_id}/allocations/")
                alloc_response = requests.get(f"{BASE_URL}/projects/{project_id}/allocations/", timeout=10)
                print(f"Status: {alloc_response.status_code}")
                
                if alloc_response.status_code == 200:
                    alloc_data = alloc_response.json()
                    print(f"✅ Allocations Success: {len(alloc_data)} allocations found")
                    
                    if alloc_data:
                        first_alloc = alloc_data[0]
                        employee = first_alloc.get('employee', {})
                        print(f"   First Employee: {employee.get('first_name')} {employee.get('last_name')}")
                        print(f"   Allocation: {first_alloc.get('allocation')}%")
                        print(f"   Department: {employee.get('department')}")
                    else:
                        print("   ℹ️ No allocations found")
                else:
                    print(f"❌ Allocations failed: {alloc_response.text}")
            
            else:
                print("ℹ️ No projects found. Create a project first.")
        else:
            print(f"❌ Failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

    print(f"\n{'='*45}")
    print("🎉 ViewProject Backend Test Complete!")
    print("If all tests passed, the ViewProject.js frontend should work correctly.")

if __name__ == "__main__":
    test_endpoints()
