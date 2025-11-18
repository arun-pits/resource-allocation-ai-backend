# Django Backend Implementation for ViewProject.js

This document outlines the complete Django backend implementation to support the ViewProject.js frontend component.

## Overview

The ViewProject.js component requires the following Django backend functionality:

-   Project detail retrieval
-   Employee allocations for a project
-   Project deletion
-   Proper error handling and data formatting

## API Endpoints

### 1. Get Project Details

**Endpoint:** `GET /api/projects/{id}/`

**Description:** Retrieves detailed information about a single project.

**Response Format:**

```json
{
	"id": 1,
	"project_id": "PROJ001",
	"project_name": "Sample Project",
	"description": "Project description",
	"project_manager": "John Doe",
	"department": "Engineering",
	"url": "https://github.com/company/project",
	"devops_url": "https://azure.devops.com/company/project",
	"start_date": "2025-01-01",
	"end_date": "2025-03-31",
	"status": "active",
	"total_allocated_percentage": 150.0,
	"team_count": 2,
	"created_at": "2025-11-18T09:30:00Z",
	"updated_at": "2025-11-18T09:30:00Z"
}
```

### 2. Get Project Allocations

**Endpoint:** `GET /api/projects/{id}/allocations/`

**Description:** Retrieves all employee allocations for a specific project.

**Response Format:**

```json
[
	{
		"id": 1,
		"employee": {
			"id": 1,
			"first_name": "John",
			"last_name": "Doe",
			"employee_email": "john.doe@company.com",
			"employee_ph_no": "+1234567890",
			"designation": "Senior Developer",
			"employee_id": "EMP001",
			"department": "Engineering",
			"manager": "Jane Smith",
			"created_at": "2025-11-18T09:30:00Z",
			"updated_at": "2025-11-18T09:30:00Z"
		},
		"allocation": "75.00",
		"created_at": "2025-11-18T09:30:00Z",
		"updated_at": "2025-11-18T09:30:00Z"
	}
]
```

### 3. Delete Project

**Endpoint:** `DELETE /api/projects/{id}/`

**Description:** Deletes a project and all its associated allocations.

**Response Format:**

```json
{
	"message": "Project deleted successfully"
}
```

## Django Implementation

### Models

#### Project Model (`apps/project/models.py`)

```python
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
```

#### ProjectAllocation Model (`apps/project/models.py`)

```python
class ProjectAllocation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='allocations')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='project_allocations')
    allocation = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Serializers

#### ProjectDetailSerializer (`apps/project/serializers.py`)

```python
class ProjectDetailSerializer(serializers.ModelSerializer):
    """Detailed project serializer for individual project view"""
    total_allocated_percentage = serializers.SerializerMethodField(read_only=True)
    team_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'project_id', 'project_name', 'description',
            'project_manager', 'department', 'url', 'devops_url',
            'start_date', 'end_date', 'status', 'total_allocated_percentage',
            'team_count', 'created_at', 'updated_at'
        ]

    def get_total_allocated_percentage(self, obj):
        """Calculate total allocated percentage for this project"""
        allocations = obj.allocations.all()
        return sum(float(alloc.allocation) for alloc in allocations) if allocations else 0

    def get_team_count(self, obj):
        """Get count of team members"""
        return obj.allocations.count()
```

#### ProjectAllocationDetailSerializer (`apps/project/serializers.py`)

```python
class ProjectAllocationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for project allocations including full employee information"""
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = ProjectAllocation
        fields = ['id', 'employee', 'allocation', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### Views

#### ProjectViewSet (`apps/project/views.py`)

The main view implementation includes:

1. **retrieve method**: Returns project details using ProjectDetailSerializer
2. **allocations action**: Custom action to return project allocations
3. **destroy method**: Handles project deletion

Key methods:

```python
def retrieve(self, request, pk=None, *args, **kwargs):
    """Get single project by ID with detailed information"""
    try:
        project = Project.objects.get(pk=pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    except Project.DoesNotExist:
        return Response({
            'message': 'Project not found'
        }, status=status.HTTP_404_NOT_FOUND)

@action(detail=True, methods=['get'])
def allocations(self, request, pk=None):
    """Get employee allocations for a specific project"""
    try:
        project = Project.objects.get(pk=pk)
        allocations = project.allocations.select_related('employee').all()
        serializer = ProjectAllocationDetailSerializer(allocations, many=True)
        return Response(serializer.data)
    except Project.DoesNotExist:
        return Response({
            'message': 'Project not found'
        }, status=status.HTTP_404_NOT_FOUND)
```

### URL Configuration

#### Project URLs (`apps/project/urls.py`)

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

#### Main URLs (`backend/urls.py`)

```python
urlpatterns = [
    path('api/', include('apps.employee.urls')),
    path('api/', include('apps.project.urls')),
    path('admin/', admin.site.urls),
]
```

## Frontend Integration

The ViewProject.js component makes the following API calls:

1. **Initial Load:**

    - `GET /api/projects/{id}/` - Load project details
    - `GET /api/projects/{id}/allocations/` - Load employee allocations

2. **User Actions:**
    - Edit button: Navigate to edit page
    - Delete button: `DELETE /api/projects/{id}/`

## Data Flow

1. **Project Loading:**

    ```javascript
    const fetchProject = async () => {
    	const response = await fetch(
    		`http://localhost:8000/api/projects/${id}/`
    	);
    	const data = await response.json();
    	setProject(data);
    };
    ```

2. **Allocations Loading:**

    ```javascript
    const fetchProjectAllocations = async () => {
    	const response = await fetch(
    		`http://localhost:8000/api/projects/${id}/allocations/`
    	);
    	const data = await response.json();
    	setAllocations(data);
    };
    ```

3. **Project Deletion:**
    ```javascript
    const handleDelete = async () => {
    	const response = await fetch(
    		`http://localhost:8000/api/projects/${id}/`,
    		{
    			method: "DELETE",
    		}
    	);
    	if (response.ok) {
    		navigate("/projects");
    	}
    };
    ```

## Error Handling

The Django backend provides consistent error responses:

-   **404 Not Found**: When project doesn't exist
-   **400 Bad Request**: For validation errors
-   **500 Internal Server Error**: For server errors

Error response format:

```json
{
	"message": "Error description"
}
```

## Testing

To test the backend implementation:

1. **Start Django Server:**

    ```bash
    cd backend
    python manage.py runserver 8000
    ```

2. **Test Endpoints:**

    - `GET http://localhost:8000/api/projects/1/`
    - `GET http://localhost:8000/api/projects/1/allocations/`
    - `DELETE http://localhost:8000/api/projects/1/`

3. **Create Test Data:**
   Use Django admin or create a management command to add test projects and employees.

## Security Considerations

-   Add authentication/authorization as needed
-   Validate user permissions for project access
-   Implement rate limiting for API calls
-   Add CORS configuration for frontend integration

## Performance Optimizations

-   Use `select_related('employee')` for allocation queries
-   Add database indexing for frequently queried fields
-   Implement caching for project details
-   Use pagination for large allocation lists

This implementation provides a robust backend foundation for the ViewProject.js frontend component with proper error handling, data validation, and optimal performance.
