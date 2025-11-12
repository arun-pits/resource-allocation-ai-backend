from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'first_name', 'last_name', 'employee_email', 'department', 'designation', 'created_at']
    list_filter = ['department', 'designation', 'created_at']
    search_fields = ['first_name', 'last_name', 'employee_email', 'employee_id']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'employee_email', 'employee_ph_no')
        }),
        ('Employment Details', {
            'fields': ('employee_id', 'designation', 'department', 'manager')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )