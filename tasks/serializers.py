from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'created_date': {'read_only': True},
            'modified_date': {'read_only': True},
        }

    def update (self, instance, validated_data):
         instance.title = validated_data.get('title', instance.title)
         instance.description = validated_data.get('description', instance.description)
         instance.priority = validated_data.get('priority', instance.priority)
         instance.save()
         return instance