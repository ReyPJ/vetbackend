from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Task, TaskCompletedProof


@receiver(post_delete, sender=Task)
def delete_file(sender, instance, **kwargs):
    if instance.help_image:
        if default_storage.exists(instance.help_image.name):
            instance.help_image.delete(save=False)


@receiver(post_delete, sender=TaskCompletedProof)
def delete_proof_file(sender, instance, **kwargs):
    if instance.proof_image:
        if default_storage.exists(instance.proof_image.name):
            instance.proof_image.delete(save=False)

