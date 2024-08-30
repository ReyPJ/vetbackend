from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsStaffOrAdmin
from .models import Task, TaskInstance
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        task = serializer.save()
        task.create_instance()

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
    def post(request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)

        if 'instance_id' not in request.data:
            return Response({'error': 'Instance ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        instance_id = request.data['instance_id']
        instance = get_object_or_404(TaskInstance, pk=instance_id, task=task)

        if task.is_recurrent:
            if 'proof_image' not in request.FILES:
                return Response({'error': 'Proof image is required'}, status=status.HTTP_400_BAD_REQUEST)

            proof_image = request.FILES['proof_image']

            if not isinstance(proof_image, InMemoryUploadedFile):
                return Response({'error': 'Invalid File Type'}, status=status.HTTP_400_BAD_REQUEST)

            instance.mark_as_completed()
            task.proof_image = proof_image
            instance.save()

            if not task.taskinstance_set.filter(is_completed=False).exists():
                task.mark_as_completed()
                task.proof_image = proof_image
                task.save()
                return Response({'status': 'Task and all instances marked as completed'}, status=status.HTTP_200_OK)

            return Response({'status': 'Instance marked as completed'}, status=status.HTTP_200_OK)
        else:
            if 'proof_image' not in request.FILES:
                return Response({'error': 'Proof image is required'}, status=status.HTTP_400_BAD_REQUEST)

            proof_image = request.FILES['proof_image']

            if not isinstance(proof_image, InMemoryUploadedFile):
                return Response({'error': 'Invalid File Type'}, status=status.HTTP_400_BAD_REQUEST)

            task.mark_as_completed()
            task.proof_image = proof_image
            task.save()

            return Response({'status': 'Task marked as completed'}, status=status.HTTP_200_OK)
