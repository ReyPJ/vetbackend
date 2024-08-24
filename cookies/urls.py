from django.urls import path
from .views import set_admin_cookie

urlpatterns = [
    path('set-admin-cookie/', set_admin_cookie, name='set-admin-cookie'),
]