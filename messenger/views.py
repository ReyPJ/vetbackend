from pyexpat.errors import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
from django.conf import settings
from tasks.models import Task
import json


class SendWhatsAppMessageAPIView(APIView):
    @staticmethod
    def post(request, task_id):
        try:
            task = Task.objects.get(id=task_id)

            if not task.assigned_to or not task.assigned_to.phone:
                return Response(
                    {"error": "No hay usuario asignado o no tiene un numero de telefono"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = task.assigned_to.username
            task_name = task.title
            variables = {
                "1": username,
                "2": task_name,
                "3": "10"
            }

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            message = client.messages.create(
                from_={settings.TWILIO_WHATSAPP_NUMBER},
                to=f"whatsapp:{task.assigned_to.phone}",
                content_sid=settings.TWILIO_TEMPLATE_ID_1,
                content_variables=json.dumps(variables)
            )

            return Response(
                {"message": f"Mensaje enviado, message sid: {message.sid}"},
                status=status.HTTP_200_OK
            )

        except Task.DoesNotExist:
            return Response(
                {"error": "La tarea no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
