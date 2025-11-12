from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# The router automatically creates these endpoints:
# GET /api/employees/ - list all employees
# POST /api/employees/ - create new employee
# GET /api/employees/{id}/ - get single employee
# PUT /api/employees/{id}/ - update entire employee
# PATCH /api/employees/{id}/ - partial update employee
# DELETE /api/employees/{id}/ - delete employee