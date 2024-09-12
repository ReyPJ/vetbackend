from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from urllib3 import request

from users.permissions import IsStaffOrAdmin
from .models import Task, TaskInstance, TaskCompletedProof
from .serializers import TaskSerializer, TaskCompletedProofSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """
    To filter the tasks list by archived status you need to pass the is_archived query parameter<br>
    (tasks/?is_archived=true) or (tasks/?is_archived=false)
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.all()
        is_archived = self.request.query_params.get('is_archived', None)
        if is_archived is not None:
            if is_archived.lower() == 'true':
                queryset = Task.objects.filter(is_archived=True)
            elif is_archived.lower() == 'false':
                queryset = Task.objects.filter(is_archived=False)
        return queryset.order_by('created_date')

    def perform_create(self, serializer):
        task = serializer.save()
        task.create_instance()

        task.scheduled_notification()


class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]

    # Habilitando Patch
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class TaskArchiveView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        task_ids = request.data.get('task_ids', [])

        if not task_ids:
            return Response({'error': 'Task IDs are required'}, status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(id__in=task_ids, is_completed=True)

        if not tasks.exists():
            return Response({'error': 'No tasks found'}, status=status.HTTP_404_NOT_FOUND)

        tasks.update(is_archived=True)

        return JsonResponse({'status': f'{tasks.count()} tasks have been archived'}, status=status.HTTP_200_OK)

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

class TaskProofListView(generics.ListAPIView):
    """
    To filter the proofs list by task you need to pass the task_id as a query parameter<br>
    (tasks/proofs/?task_id=1)
    """
    queryset = TaskCompletedProof.objects.all()
    serializer_class = TaskCompletedProofSerializer
    permission_classes = [IsAuthenticated]

    # Filter the proofs list y task id
    def get_queryset(self):
        task_id = self.request.query_params.get('task_id', None)
        if task_id is not None:
            return TaskCompletedProof.objects.filter(task_id=task_id)
        return TaskCompletedProof.objects.all().order_by('-completed_date')

class TaskProofDetailView(generics.RetrieveAPIView):
    queryset = TaskCompletedProof.objects.all()
    serializer_class = TaskCompletedProofSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskCompletedProof.objects.all().order_by('-completed_date')

class TaskMarkAsCompleted(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        user = request.user
        notes = request.data.get('notes', '')

        if task.is_recurrent:
            if 'instance_id' not in request.data:
                return Response({'error': 'Instance ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            instance_id = request.data['instance_id']
            instance = get_object_or_404(TaskInstance, pk=instance_id, task=task)

            if 'proof_image' not in request.FILES:
                return Response({'error': 'Proof image is required'}, status=status.HTTP_400_BAD_REQUEST)

            proof_image = request.FILES['proof_image']

            if not isinstance(proof_image, InMemoryUploadedFile):
                return Response({'error': 'Invalid File Type'}, status=status.HTTP_400_BAD_REQUEST)

            instance.mark_as_completed()
            task.proof_image = proof_image
            instance.save()

            TaskCompletedProof.objects.create(task=task, proof_image=proof_image, user=user, notes=notes)

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

            TaskCompletedProof.objects.create(task=task, proof_image=proof_image, user=user, notes=notes)
            task.mark_as_completed()
            task.proof_image = proof_image
            task.save()

            return Response({'status': 'Task marked as completed'}, status=status.HTTP_200_OK)
