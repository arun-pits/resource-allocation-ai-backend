from django.contrib import admin
from .models import Project, ProjectAllocation

class ProjectAllocationInline(admin.TabularInline):
    model = ProjectAllocation
    extra = 1
    raw_id_fields = ['employee']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_id', 'project_name', 'project_manager', 'department', 'status', 'start_date', 'end_date', 'allocations_count']
    list_filter = ['status', 'department', 'start_date', 'end_date']
    search_fields = ['project_id', 'project_name', 'project_manager']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    inlines = [ProjectAllocationInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project_id', 'project_name', 'description')
        }),
        ('Project Details', {
            'fields': ('project_manager', 'department', 'status')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('URLs', {
            'fields': ('url', 'devops_url'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def allocations_count(self, obj):
        return obj.allocations.count()
    allocations_count.short_description = 'Team Members'

@admin.register(ProjectAllocation)
class ProjectAllocationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'project', 'allocation', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name', 'project__project_name']
    raw_id_fields = ['employee', 'project']
    readonly_fields = ['created_at', 'updated_at']