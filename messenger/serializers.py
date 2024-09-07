from rest_framework import serializers


class WhatsAppMessageSerializer(serializers.Serializer):
    to = serializers.CharField(max_length=50)

    param1 = serializers.CharField(required=False)
    param2 = serializers.CharField(required=False)
