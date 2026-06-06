from django.db import models

# Create your models here.

class Project(models.Model):
    """Model representing a travel project."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def is_completed(self):
        places = self.places.all()
        if not places.exists():
            return False
        return all(place.is_visited for place in places)
            
    
class Place(models.Model):
    """Model representing a place to visit."""
    project = models.ForeignKey(Project, related_name='places', on_delete=models.CASCADE)
    
    external_id = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.external_id} in {self.project.name} ({'Visited' if self.is_visited else 'Not Visited'})"