from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, employee_projects_view

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Use either the class-based action or function-based view, not both
    
    # Option 1: Using the class-based action (recommended)
    # The action is automatically available at: /api/employees/{id}/projects/
    
    # Option 2: Using function-based view (if you prefer this)
    path('employees/<int:employee_id>/projects/', employee_projects_view, name='employee-projects'),
]