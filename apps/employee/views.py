from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Get single employee by ID
        """
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = self.get_serializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({
                'message': 'Employee not found'
            }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Update employee - supports both PUT (full update) and PATCH (partial update)
        """
        try:
            employee = Employee.objects.get(pk=pk)
            partial = kwargs.pop('partial', False)
            
            # Check if email is being changed and if it already exists for another employee
            if 'employee_email' in request.data and request.data['employee_email'] != employee.employee_email:
                if Employee.objects.filter(employee_email=request.data['employee_email']).exclude(pk=pk).exists():
                    return Response({
                        'message': 'Error updating employee',
                        'errors': {'employee_email': ['Employee with this email already exists.']}
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if employee_id is being changed and if it already exists for another employee
            if 'employee_id' in request.data and request.data['employee_id'] != employee.employee_id:
                if Employee.objects.filter(employee_id=request.data['employee_id']).exclude(pk=pk).exists():
                    return Response({
                        'message': 'Error updating employee',
                        'errors': {'employee_id': ['Employee with this ID already exists.']}
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(employee, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Employee updated successfully',
                    'data': serializer.data
                })
            return Response({
                'message': 'Error updating employee',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Employee.DoesNotExist:
            return Response({
                'message': 'Employee not found'
            }, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Handle PATCH requests for partial updates
        """
        kwargs['partial'] = True
        return self.update(request, pk, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create new employee
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Employee created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Error creating employee',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Get all employees
        """
        employees = self.get_queryset()
        serializer = self.get_serializer(employees, many=True)
        return Response({
            'count': employees.count(),
            'employees': serializer.data
        })

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete employee
        """
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            return Response({
                'message': 'Employee deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({
                'message': 'Employee not found'
            }, status=status.HTTP_404_NOT_FOUND)