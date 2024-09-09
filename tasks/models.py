from django.db import models
from users.models import CustomUser
from datetime import timedelta


class Task(models.Model):
    VERY_IMPORTANT = 2
    IMPORTANT = 1
    NOT_IMPORTANT = 0

    PRIO_CHOICES = [
        (VERY_IMPORTANT, 'Very important'),
        (IMPORTANT, 'Important'),
        (NOT_IMPORTANT, 'Not important'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=800, blank=True, null=True, default=None)
    priority = models.IntegerField(choices=PRIO_CHOICES, default=NOT_IMPORTANT)
    is_completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    scheduled_start_date = models.DateTimeField(blank=True, null=True, default=None)
    modified_date = models.DateTimeField(auto_now=True)
    help_image = models.ImageField(upload_to='tasks/', blank=True, null=True)
    is_recurrent = models.BooleanField(default=False)
    recurrent_period = models.DurationField(blank=True, null=True, default=None)
    recurrent_days = models.IntegerField(default=1)
    proof_image = models.ImageField(upload_to='tasks/proofs/', blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="assigned_tasks",
        blank=True,
        null=True
    )

    def mark_as_completed(self):
        self.is_completed = True
        self.save()

    def mark_as_uncompleted(self):
        self.is_completed = False
        self.save()

    def create_instance(self):
        if self.is_recurrent and self.recurrent_period:
            recurrence_hours = self.recurrent_period.total_seconds() / 3600.0
            total_instances = int((self.recurrent_days * 24) / recurrence_hours)

            for i in range(total_instances):
                scheduled_time = self.created_date + timedelta(hours=recurrence_hours * i)
                TaskInstance.objects.create(task=self, instance_number=i + 1, scheduled_time=scheduled_time)


class TaskInstance(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    instance_number = models.IntegerField()
    scheduled_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def mark_as_completed(self):
        self.is_completed = True
        self.save()


class TaskCompletedProof(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    proof_image = models.ImageField(upload_to='tasks/proofs/', blank=True, null=True)
    completed_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=800, blank=True, null=True, default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.user.username} - {self.task}'
