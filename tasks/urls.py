from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDestroyView,
    TaskMarkAsCompleted,
    TaskDetailView,
    TaskUpdateView,
    TaskProofListView,
    TaskProofDetailView,
    TaskArchiveView
)

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/proofs/', TaskProofListView.as_view(), name='task-proofs'),
    path('tasks/proofs/<int:pk>/', TaskProofDetailView.as_view(), name='task-proof-detail'),
    path('tasks/<int:pk>/delete/', TaskDestroyView.as_view(), name='task-destroy'),
    path('tasks/<int:pk>/detail/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/mark-as-completed/', TaskMarkAsCompleted.as_view(), name='task-mark-as-completed'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/archive/', TaskArchiveView.as_view(), name='task-archive'),
]

