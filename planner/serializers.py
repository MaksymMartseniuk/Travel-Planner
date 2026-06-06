import os
import requests
from rest_framework import serializers
from .models import Project, Place

ART_API_URL = os.getenv('ART_API_URL', 'https://api.artic.edu/api/v1/artworks')

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'external_id', 'notes', 'is_visited']
        read_only_fields = ['id']

class ProjectSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, required=False)

    is_completed = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'is_completed', 'places']
        read_only_fields = ['id', 'is_completed']
    
    def validate_places(self, places_data):

        if len(places_data) > 10:
            raise serializers.ValidationError("Maximum of 10 places allowed per project.")

        external_ids = [place.get('external_id') for place in places_data]
        if len(external_ids) != len(set(external_ids)):
            raise serializers.ValidationError("There are duplicate places in the request (same external_id).")

        for ext_id in external_ids:
            try:
                response = requests.get(f"{ART_API_URL}/{ext_id}", timeout=5)
                if response.status_code != 200:
                    raise serializers.ValidationError(
                        f"Place with ID {ext_id} not found in Art Institute API."
                    )
            except requests.RequestException:
                raise serializers.ValidationError(
                    "Error connecting to external API for place validation."
                )

        return places_data
    
    def create(self, validated_data):
        places_data = validated_data.pop('places', [])
        project = Project.objects.create(**validated_data)
        
        for place_data in places_data:
            Place.objects.create(project=project, **place_data)
            
        return project