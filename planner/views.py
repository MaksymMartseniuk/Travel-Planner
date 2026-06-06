from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Project, Place
from .serializers import ProjectSerializer, PlaceSerializer
# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    """Auto-generated viewset for Project model."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def destroy(self, request, *args, **kwargs):
        """Override the destroy method to prevent deletion of projects with visited places."""
        project = self.get_object()
        
        if project.places.filter(is_visited=True).exists():
            return Response(
                {"detail": "Cannot delete project: some places are already marked as visited."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)
    
class PlaceViewSet(viewsets.ModelViewSet):
    """Auto-generated viewset for Place model."""
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_queryset(self):
        """Optionally filter places by project_id query parameter."""
        queryset = super().get_queryset()
        project_id = self.request.query_params.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset
