import os
import requests
from rest_framework import serializers
from .models import Project, Place

ART_API_URL = os.getenv('ART_API_URL', 'https://api.artic.edu/api/v1/artworks')

def validate_external_place(external_id):
    try:
        response = requests.get(f"{ART_API_URL}/{external_id}", timeout=5)
        if response.status_code != 200:
            raise serializers.ValidationError(f"Place with ID {external_id} not found in Art Institute API.")
    except requests.RequestException:
        raise serializers.ValidationError("Error connecting to external API for place validation.")

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'project', 'external_id', 'notes', 'is_visited']
        read_only_fields = ['id']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.method in ['PUT', 'PATCH']:
            fields['project'].read_only = True
            fields['external_id'].read_only = True
        return fields

    def validate(self, attrs):
        if self.instance is None: 
            project = attrs.get('project')
            external_id = attrs.get('external_id')

            if project.places.count() >= 10:
                raise serializers.ValidationError({"detail": "Maximum of 10 places allowed per project."})
            
            if Place.objects.filter(project=project, external_id=external_id).exists():
                raise serializers.ValidationError({"detail": "This place is already added to this project."})
            
            validate_external_place(external_id)

        return attrs


class PlaceNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'external_id', 'notes', 'is_visited']
        read_only_fields = ['id']

class ProjectSerializer(serializers.ModelSerializer):
    places = PlaceNestedSerializer(many=True, required=False)

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
            validate_external_place(ext_id)

        return places_data
    
    def create(self, validated_data):
        places_data = validated_data.pop('places', [])
        project = Project.objects.create(**validated_data)
        
        for place_data in places_data:
            Place.objects.create(project=project, **place_data)
            
        return project