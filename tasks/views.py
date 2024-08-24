from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from users.permissions import IsStaffOrAdmin
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]

class TaskDetailDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response({'status': 'Task deleted'}, status=status.HTTP_204_NO_CONTENT)