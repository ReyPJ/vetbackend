import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Task, TaskCompletedProof

@receiver(post_delete, sender=Task)
def delete_file(sender, instance, **kwargs):
    if instance.help_image:
        if os.path.isfile(instance.help_image.path):
            os.remove(instance.help_image.path)


@receiver(post_delete, sender=TaskCompletedProof)
def delete_proof_file(sender, instance, **kwargs):
    if instance.proof_image:
        if os.path.isfile(instance.proof_image.path):
            os.remove(instance.proof_image.path)