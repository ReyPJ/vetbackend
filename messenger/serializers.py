from rest_framework import serializers


class WhatsAppMessageSerializer(serializers.Serializer):
    to = serializers.CharField(max_length=50)
    variables = serializers.DictField(child=serializers.CharField(), required=False)
