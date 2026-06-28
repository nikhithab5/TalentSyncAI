from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


def generate_tsa_id():
    last_profile = Profile.objects.exclude(
        tsa_id__isnull=True
    ).order_by('-id').first()

    if last_profile and last_profile.tsa_id:
        last_number = int(last_profile.tsa_id.replace("TSA", ""))
        new_number = last_number + 1
    else:
        new_number = 1

    return f"TSA{new_number:06d}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            tsa_id=generate_tsa_id()
        )