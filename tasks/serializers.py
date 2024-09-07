from rest_framework import serializers
from .models import Task, TaskInstance, TaskCompletedProof


class TaskInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInstance
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    instances = TaskInstanceSerializer(many=True, read_only=True, source='taskinstance_set')

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'created_date': {'read_only': True},
            'modified_date': {'read_only': True},
        }

    def update(self, instance, validated_data):
         instance.title = validated_data.get('title', instance.title)
         instance.description = validated_data.get('description', instance.description)
         instance.priority = validated_data.get('priority', instance.priority)
         instance.save()
         return instance

class TaskCompletedProofSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TaskCompletedProof
        fields = "__all__"
