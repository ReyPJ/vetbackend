from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
from django.conf import settings
from .serializers import WhatsAppMessageSerializer
import json


class SendWhatsAppMessageAPIView(APIView):
    def post(self, request):
        serializer = WhatsAppMessageSerializer(data=request.data)

        if serializer.is_valid():
            to = serializer.validated_data.get("to")

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            try:
                message = client.messages.create(
                    from_=settings.TWILIO_WHATSAPP_NUMBER,
                    to=f"whatsapp:{to}",
                    content_sid=settings.TWILIO_TEMPLATE_ID_1,
                    content_variables=json.dumps(
                        {
                            "1": "Reyner",
                            "2": "Limpiar internados",
                            "3": "20 minutos",
                        }
                    )
                )
                return Response({f"Mensaje enviado, message_sid: {message.sid}"}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
