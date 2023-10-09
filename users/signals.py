from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def add_to_group(sender, instance, created, **kwargs):
    if created:
       group = Group.objects.get(name='customer')
       instance.groups.add(group)