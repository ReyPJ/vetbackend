from django.urls import path
from .views import SendWhatsAppMessageAPIView

urlpatterns = [
    path("send-whatsapp/", SendWhatsAppMessageAPIView.as_view(), name="send-whatsapp-message"),
]
