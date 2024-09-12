from celery import shared_task
from django.urls import reverse
import requests


@shared_task
def send_whatsapp_notification(task_id):
    url = "http://localhost:8000/api" + reverse("send-whatsapp", args=[task_id])

    try:
        response = requests.post(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error enviando la notificacion para la tarea {task_id}: {str(e)}")
