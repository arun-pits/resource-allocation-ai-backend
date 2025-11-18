from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Project, ProjectAllocation
from .serializers import (
    ProjectSerializer,
    ProjectAllocationSerializer,
    ProjectAllocationDetailSerializer,
    ProjectDetailSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        print("=== PROJECT CREATE VIEW ===")
        print(f"Request data: {request.data}")

        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)

                if serializer.is_valid():
                    print("Serializer is valid")
                    project = serializer.save()
                    print(f"Project saved: {project.id}")

                    allocations_count = project.allocations.count()
                    print(f"Allocations in database: {allocations_count}")

                    project_data = self.get_serializer(project).data

                    return Response({
                        'message': 'Project created successfully',
                        'data': project_data,
                        'allocations_created': allocations_count
                    }, status=status.HTTP_201_CREATED)
                else:
                    print(f"Serializer errors: {serializer.errors}")
                    return Response({
                        'message': 'Error creating project',
                        'errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Exception in project creation: {str(e)}")
            return Response({
                'message': 'Error creating project',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        projects = self.get_queryset()
        serializer = self.get_serializer(projects, many=True)
        return Response({
            'count': projects.count(),
            'projects': serializer.data
        })

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            project = Project.objects.get(pk=pk)
            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, *args, **kwargs):
        print("=== PROJECT UPDATE VIEW ===")
        print(f"Project ID: {pk}")
        print(f"Request data: {request.data}")

        try:
            with transaction.atomic():
                project = Project.objects.get(pk=pk)
                serializer = self.get_serializer(
                    project, data=request.data, partial=kwargs.pop('partial', False)
                )

                if serializer.is_valid():
                    project = serializer.save()
                    allocations_count = project.allocations.count()

                    return Response({
                        'message': 'Project updated successfully',
                        'data': self.get_serializer(project).data,
                        'allocations_count': allocations_count
                    })

                return Response({
                    'message': 'Error updating project',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'message': 'Error updating project',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return Response({'message': 'Project deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def allocations(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            allocations = project.allocations.select_related('employee').all()
            serializer = ProjectAllocationDetailSerializer(allocations, many=True)

            return Response({
                'project_id': project.project_id,
                'project_name': project.project_name,
                'allocations': serializer.data,
                'total_allocations': len(serializer.data)
            })

        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def team_members(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            allocations = project.allocations.all()
            serializer = ProjectAllocationSerializer(allocations, many=True)

            return Response({
                'project_id': project.project_id,
                'project_name': project.project_name,
                'team_members': serializer.data,
                'total_members': allocations.count()
            })

        except Project.DoesNotExist:
            return Response({'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def active_projects(self, request):
        active_projects = Project.objects.filter(status='active')
        serializer = self.get_serializer(active_projects, many=True)
        return Response({
            'count': active_projects.count(),
            'projects': serializer.data
        })
