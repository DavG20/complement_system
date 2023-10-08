from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
active_roles = (("user", "user"), ("manager", "manager"))


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=120, choices=active_roles, default="user")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = getattr(instance, "role", "user")

        # Check if the user is an admin
        if instance.is_staff and instance.is_superuser:
            role = "admin"

        _ = profile.objects.create(user=instance, role=role)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        Profile = instance.profile
        Profile.save()
    except profile.DoesNotExist:
        pass
