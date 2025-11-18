from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.employee.models import Employee

class Project(models.Model):
    PROJECT_STATUS = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    project_id = models.CharField(max_length=50, unique=True)
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    project_manager = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    devops_url = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='planning')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project_name} ({self.project_id})"

class ProjectAllocation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='allocations')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='project_allocations')
    allocation = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Allocation percentage (0-100)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_allocations'
        unique_together = ['project', 'employee']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee} - {self.project}: {self.allocation}%"