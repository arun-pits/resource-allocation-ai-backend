from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    employee_email = models.EmailField(unique=True)
    employee_ph_no = models.CharField(max_length=15)
    designation = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    manager = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"