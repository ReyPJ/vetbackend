from django.db import models
from users.models import CustomUser

class Task(models.Model):
    VERY_IMPORTANT = 2
    IMPORTANT = 1
    NOT_IMPORTANT = 0

    PRIO_CHOICES = [
        (VERY_IMPORTANT, 'Very important'),
        (IMPORTANT, 'Important'),
        (NOT_IMPORTANT, 'Not important'),
    ]

    title= models.CharField(max_length=100)
    description= models.TextField(max_length=800, blank=True, null=True, default=None)
    priority= models.IntegerField(choices=PRIO_CHOICES, default=NOT_IMPORTANT)
    is_completed= models.BooleanField(default=False)
    created_date= models.DateTimeField(auto_now_add=True)
    modified_date= models.DateTimeField(auto_now=True)
    help_image = models.ImageField(upload_to='static/tasks/', blank=True, null=True)
    is_recurrent = models.BooleanField(default=False)
    recurrent_period = models.DurationField(blank=True, null=True, default=None)

    def mark_as_completed(self):
        self.is_completed = True
        self.save()

    def mark_as_uncompleted(self):
        self.is_completed = False
        self.save()
