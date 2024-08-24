from django.urls import path
from .views import TaskListCreateView, TaskDetailDestroyView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailDestroyView.as_view(), name='task-detail'),
]