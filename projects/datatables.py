from rest_framework import serializers
from .models import Project, Technology

class TechnolgySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Technology
        fields = (
            'id','name'
        )
        
class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    technologies = TechnolgySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'name','technologies'
        )
