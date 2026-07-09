from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment


@receiver(post_save, sender=Appointment)
def mark_completed_status(sender, instance: Appointment, created: bool, **kwargs):
    if created and instance.fee == 0 and instance.status != "completed":
        instance.status = "completed"
        instance.save(update_fields=["status"])
