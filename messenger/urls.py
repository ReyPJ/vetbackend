from django.urls import path
from .views import SendWhatsAppMessageAPIView

urlpatterns = [
    path("send-whatsapp/<int:task_id>/", SendWhatsAppMessageAPIView.as_view(), name="send-whatsapp-message"),
]
