from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

"""
    Here in signals.py we are creating signal so that
    when the user get register to out website we automatically
    the Profile page of that use and save the instance of that 
    user into the databas. 

"""

@receiver(post_save,sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)


@receiver(post_save,sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
