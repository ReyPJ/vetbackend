from django.urls import path
from .views import UserListCreateView, UserDetailView, ChangePasswordView, UsernamesListView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('usernames/', UsernamesListView.as_view(), name='usernames-list'),
]