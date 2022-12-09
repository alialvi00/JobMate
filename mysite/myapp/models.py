from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Database model Users has one to one relationship with Django User table
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField()
    password1 = models.TextField()
    password2 = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()