from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsStaffOrAdmin
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]

    # Habilitando Patch
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class TaskDestroyView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response({'status': 'Task deleted'}, status=status.HTTP_204_NO_CONTENT)

class TaskMarkAsCompleted(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        if 'proof_image' not in request.FILES:
            return Response({'error': 'Proof image is required'}, status=status.HTTP_400_BAD_REQUEST)

        proof_image = request.FILES['proof_image']

        if not isinstance(proof_image, InMemoryUploadedFile):
            return Response({'error': 'Invalid File Type'}, status=status.HTTP_400_BAD_REQUEST)

        task.mark_as_completed()
        task.proof_image = proof_image
        task.save()
        task.mark_as_completed()
        return Response({'status': 'Task marked as completed'}, status=status.HTTP_200_OK)