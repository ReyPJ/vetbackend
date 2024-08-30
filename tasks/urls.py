from django.urls import path
from .views import TaskListCreateView, TaskDestroyView, TaskMarkAsCompleted, TaskDetailView, TaskUpdateView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDestroyView.as_view(), name='task-destroy'),
    path('tasks/<int:pk>/detail/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/mark-as-completed/', TaskMarkAsCompleted.as_view(), name='task-mark-as-completed'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
]