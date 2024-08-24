from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {
            'created_date': {'read_only': True},
        }

    def create(self, validated_data):
        try:
            task = Task(
                title=validated_data['title'],
                description=validated_data['description'],
                priority=validated_data['priority'],
                is_completed=validated_data['is_completed'],
                is_recurrent=validated_data['is_recurrent'],
                recurrent_period=validated_data['recurrent_period']
            )
            task.save()
            return task
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def update(self, instance, validated_data):
        try:
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.priority = validated_data.get('priority', instance.priority)
            instance.is_completed = validated_data.get('is_completed', instance.is_completed)
            instance.created_by = validated_data.get('created_by', instance.created_by)
            instance.help_image = validated_data.get('help_image', instance.help_image)
            instance.is_recurrent = validated_data.get('is_recurrent', instance.is_recurrent)
            instance.recurrent_period = validated_data.get('recurrent_period', instance.recurrent_period)

            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
